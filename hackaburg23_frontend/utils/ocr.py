import os
import cv2
import numpy as np
import re
import pandas as pd
import pytesseract
from matplotlib import pyplot as plt
from pytesseract import Output
from scipy import ndimage


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

def img_txt_rec_func(img):
    
    #try:
    #    osd = pytesseract.image_to_osd(img, lang="deu")
    #    angle = re.search('(?<=Rotate: )\d+', osd).group(0)
    #except:
    #    angle = '90'

    img = ndimage.rotate(img, -int(90))
    img = img[40:200, 150:430]
    gray = get_grayscale(img)
    thresh = thresholding(gray)
    text_img = pytesseract.image_to_string(img, lang="deu") #config='-c tessedit_char_whitelist=0123456789ABCDEF.-') #--oem 0,
    text_tresh = pytesseract.image_to_string(thresh, lang="deu") 
    #text = text.replace(",", "." )
    #text = text.replace("i", "1" )
    #print(text)

    r1 = re.search(r"[0-9]{5}", text_tresh)
    if(r1 == None):
        r1 = re.search(r"[0-9]{5}", text_img)
    if(r1 != None):
        r1 = r1.group()
    r2 = re.search(r"((\d{2}(\.|,)){2}\d{2})", text_tresh)
    if(r2 == None):
        r2 = re.search(r"[0-9]{5}", text_img)
    if(r2 != None):
        r2 = r2.group()
        r2 = r2.replace(",", ".")
    r3 = re.search(r"DE", text_tresh)
    if(r3 == None):
        r3 = re.search(r"[0-9]{5}", text_img)
    if(r3 != None):
        r3 = r3.group()
    r4 = re.search(r"(\w{13})", text_tresh)
    if(r4 == None):
        r4 = re.search(r"[0-9]{5}", text_img)
    if(r4 != None):
        r4 = r4.group()
    r5 = re.search(r"\d{7}(\.|-)(\d{2}|\di)", text_tresh)
    if(r5 == None):
        r5 = re.search(r"[0-9]{5}", text_img)
    if(r5 != None):
        r5 = r5.group()
        r5 = r5.replace(".", "-")
        r5 = r5.replace("i", "1" )

    #print(r1)
    #print(r2)
    #print(r3)
    #print(r4)
    #print(r5)
    
    return text_img,text_tresh,r1,r2,r3,r4,r5,img,