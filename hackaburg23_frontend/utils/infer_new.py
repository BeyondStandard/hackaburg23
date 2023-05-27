import glob
import torch
import numpy as np
import pandas as pd
import pytorch_lightning as pl
from torch import nn
from torch.nn import functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image

MODEL_PATH="/home/ec2-user/anomaly-detection/tb_logs/my_model/version_15/checkpoints/epoch=9-step=25020.ckpt"

TRANSFORM = transforms.Compose([
    transforms.Resize((512, 512)),
    transforms.ToTensor(),
])

BRIGHTNESS_LEVELS = [0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2]
CONTRAST_LEVELS = [0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3]

np.random.shuffle(BRIGHTNESS_LEVELS)
np.random.shuffle(CONTRAST_LEVELS)


class ValidationDataset(Dataset):
    def __init__(self, directory):
        self.image_paths = glob.glob(directory + '/*.png')

        all_photos = pd.read_csv('/home/ec2-user/train_df.csv')
        self.labels = []

        for path in self.image_paths:
            filename = path.split('/')[-1]
            label = all_photos[all_photos['file'] == filename]['label'].values[0]
            self.labels.append(0 if label == 1 else 1)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img = Image.open(self.image_paths[idx]).convert('L')
        return TRANSFORM(img), self.labels[idx]


class AnomalyDetector(pl.LightningModule):
    def __init__(self):
        super(AnomalyDetector, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(128 * 64 * 64, 128)
        self.fc2 = nn.Linear(128, 2)

        self.val_dataset = ValidationDataset('/home/ec2-user/data/validation')

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=25, num_workers=16)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.conv3(x))
        x = F.max_pool2d(x, 2)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def training_step(self, batch, batch_idx):
        images, labels = batch
        logits = self(images)
        loss = F.cross_entropy(logits, labels)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        images, labels = batch
        logits = self(images)
        loss = F.cross_entropy(logits, labels)
        self.log('val_loss', loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.001)



def infer(image_path: str) -> float:
    model = AnomalyDetector.load_from_checkpoint(MODEL_PATH)
    model.eval()

    image = Image.open(image_path)
    image = TRANSFORM(image)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    image = image.unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)

    return torch.sigmoid(output)
