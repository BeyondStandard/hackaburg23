import base64
import time
import cv2
import dash_bootstrap_components as dbc
import json
import os
import pandas as pd
from dash import Dash, html, dcc, Output, Input, callback_context, ALL, MATCH, State
from dash_extensions import BeforeAfter
from dash_extensions.enrich import DashProxy

from typing import Optional

from utils.ocr import img_txt_rec_func

PRIMARY_COLOR = "#ffa500"
BACKGROUND_COLOR = "#FFFFFF"
SECONDARY_BG_COLOR = "#cdcdcd"


external_stylesheets = [dbc.themes.BOOTSTRAP]
app = DashProxy(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks=True)

LOGO = app.get_asset_url("logo.png")
GOOD_PART_LOGO = app.get_asset_url("good_part.png")
DEFECTIVE_PART_LOGO = app.get_asset_url("defective_part.png")
THUMBNAIL_LOGO = app.get_asset_url("thumbnail.png")
DEFAULT_PART = app.get_asset_url("default.png")
ERROR_CODES = app.get_asset_url("error_codes.png")
SUCCESS_CODES = app.get_asset_url("success_codes.png")
LOADING_SCREEN = app.get_asset_url("loading.gif")

def get_data():
    return pd.read_csv("hackaburg23_frontend/assets/data.csv", sep=",")

def get_thumbnail_button(item_uuid: str, filename: str, label: int):
    return html.A([
        dbc.Col(html.Img(src=(GOOD_PART_LOGO if label == 1 else DEFECTIVE_PART_LOGO), width="64px", height="64px")),
        dbc.Col(html.B(filename, style={"font-size": "12px"}))
    ],
    href="#",
    id={"type": "component", "index": item_uuid},
    style={
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "text-align": "center",

    })

data = get_data()
good_data = data.loc[data['label'] == 1].head(49) 
bad_data = data.loc[data['label'] != 1]
total_subset = pd.concat([good_data, bad_data], ignore_index=True)
total_subset['result'] = total_subset.apply(lambda row: dbc.Row(
    [get_thumbnail_button(row["id"], row["file"], row["label"])],
    id={"type": "row", "index": row["id"]}
), axis=1)

defective_parts = total_subset.loc[total_subset["label"] != 1]
good_parts = total_subset.loc[total_subset["label"] == 1]

filter_box = html.Div(
    [
        html.H2("Files", style={"font-family": "StagSans"}),
        html.P("Select your choice")
    ],
    style={
        "background-color": PRIMARY_COLOR,
        "padding": "1rem",
        "border-radius": "15px"
    }
)

thumbnail_box = html.Div(
    [
        dbc.Tabs(
            [
                # dbc.Tab(label="All", children=[
                #     dbc.Card(dbc.CardBody(
                #         all_parts
                #     ))
                # ]),
                dbc.Tab(label="Good", children=[
                    dbc.Card(dbc.CardBody(
                        good_parts['result'].to_list(), style={"display": "flex", "flex-direction": "column", "gap": "0.5rem"}
                    ))
                ]),
                dbc.Tab(label="Bad", children=[
                    dbc.Card(dbc.CardBody(
                        defective_parts['result'].to_list(), style={"display": "flex", "flex-direction": "column", "gap": "0.5rem"}
                    ))
                ])
            ],
        )
    ],
    style={
        "height": "100vh",
        "overflow": "scroll"
    }
)

sidebar = html.Div(children=
    [
        dbc.Row([filter_box]),
        dbc.Row([thumbnail_box])
    ],
    style={
        "width": "16rem",
        "padding": "1.5rem",
        "background-color": "#FFFFFF",
        "display": "flex",
        "flex-direction": "column",
        "gap": "1rem"
    }
)

main_logo = html.Img(src=LOGO, id="logo")

left = dbc.Col(children=[
    html.Div(className="top-left", children=
            [
                html.Div([main_logo], style={"background-color": PRIMARY_COLOR})
            ]),
    html.Div(className="bottom", children=[sidebar])
])

main_content = dcc.Loading(id="loading-output", children=[
    dbc.Col(
        [
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(id="main-content-picture", style={"align-items": "center", "justify-content": "center", "text-align": "center"}),
                        dbc.Col(
                            [
                                html.H2("Filename:"),
                                html.P("-", id="main-content-filename"),
                                html.H2("Serial No.:"),
                                html.P("-", id="main-content-serialnumber"),
                                html.H2("Certainty"),
                                html.P("-", id="main-content-certainty"),
                                html.H2("Verdict:"),
                                html.Div([], id="main-content-defectcode")
                            ],
                            style={
                                "backgroundColor": "#f0f0f0",
                                "padding": "1rem",
                                "margin": "1rem"
                            }
                        )
                    ]
                )
            )
        ],
        style={
            "padding": "1rem"
        }
    )]
)

header_fill = html.Span(
    style={
        "background-color": PRIMARY_COLOR,
        "height": "5rem",
        "width": "100vw"
    }
)

right = dbc.Col(id="right", className="column", children=[
    html.Div(className="top-right", children=[header_fill]),
    html.Div(className="bottom", children=[main_content])
])

app.layout = html.Div(
    [
        left,
        right
    ],
    style={
        "height": "100vh",
        "display": "flex",
        "overflow": "hidden",
        "margin": "0px",
        "display": "flex",
        "box-sizing": "border-box"
    }
)

# @app.callback(
#     Output("loading-output", "children"),
#     Input({'type': 'component', 'index': ALL}, 'n_clicks')
# )
# def loading(n):
#     time.sleep(10)
#     return html.Div(
#         [
#             html.Img(src=LOADING_SCREEN),
#             html.H3("Loading...")
#         ]
#     )

@app.callback(
    Output("main-content-picture", "children"),
    Output("main-content-filename", "children"),
    Output("main-content-serialnumber", "children"),
    Output("main-content-certainty", "children"),
    Output("main-content-defectcode", "children"),
    Input({'type': 'component', 'index': ALL}, 'n_clicks'),
    # State({'type': 'component', 'index': MATCH}, 'id')
)
def get_single_part(id: str, *args):
    if id is None:
        return "", "-", "-", "-", "-"
    
    tmp_trigger_obj = json.loads(callback_context.triggered[0]["prop_id"].split('.')[0])

    id = tmp_trigger_obj["index"]

    target_obj = data.loc[data["id"] == id]

    filename = target_obj["file"].values[0]
    serialnumber = "-"
    certainty = "-"
    defectcode = html.Img(src=(ERROR_CODES if target_obj["label"].values[0] != 1 else SUCCESS_CODES),
                          style={
                              "max-width": "360px"
                          })
    
    if filename in os.listdir("/home/ec2-user/golden_data/"):
        picture_path = f"/home/ec2-user/golden_data/{filename}"
        defect_path = f"/home/ec2-user/golden_data/{os.path.splitext(filename)[0]}-defect.png"

        with open(picture_path, "rb") as good_file, open(defect_path, "rb") as bad_file:
            good_file_data = f"data:image/png;base64, {base64.b64encode(good_file.read()).decode()}"
            bad_file_data = f"data:image/png;base64, {base64.b64encode(bad_file.read()).decode()}"

        pic = html.Div([
            BeforeAfter(before=dict(src=good_file_data), after=dict(src=bad_file_data), width="512", height="512", value=50, hover=False)
        ])
    else:
        if target_obj["label"].values[0]== 1:
            picture_path = f"/home/ec2-user/data/golden/{filename}"
        else:
            picture_path = f"/home/ec2-user/data/defect/others/{filename}"

        with open(picture_path, "rb") as f:
            pic_data = f"data:image/png;base64, {base64.b64encode(f.read()).decode()}"

        pic = html.Div([
            BeforeAfter(before=dict(src=pic_data), after=dict(src=DEFAULT_PART), width="512", height="512", value=95, hover=False)
        ])

    try:
        img = cv2.imread(picture_path)
        _, _, p1, p2, p3, p4, p5, _ = img_txt_rec_func(img)
        serialnumber = html.P(f"""
        {p1} {p2}
        {p3} {p4}
        {p5}
        """)
    except Exception as e:
        print("Failed to hand over to pytesseract.")
        print(e)

    return pic, filename, serialnumber, certainty, defectcode

if __name__ == "__main__":
    app.run_server(debug=True, port="51475")
