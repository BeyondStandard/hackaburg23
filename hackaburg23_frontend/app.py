from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


MAIN_LOGO = "images/logo.png"

PRIMARY_COLOR = "#ffa500"
BACKGROUND_COLOR = "#FFFFFF"
SECONDARY_BG_COLOR = "#969696"


external_stylesheets = ["style.css", dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)


filter_box = html.Div(id="filter-box", children=
    [
        html.H2("Files"),
        html.P("Select your choice"),
    ],
    style = {
        "padding": "1rem 1rem",
        "background-color": PRIMARY_COLOR, 
        "border-radius": "10px"
    }
)


all_thumbnails = dbc.Card(
    dbc.CardBody(
        [html.P("All")]
    ),
    className="mt-3",
)

good_thumbnails = dbc.Card(
    dbc.CardBody(
        [html.P("Good")]
    ),
    className="mt-3",
)

bad_thumbnails = dbc.Card(
    dbc.CardBody(
        [html.P("Bad")]
    ),
    className="mt-3",
)

thumbnail_box = html.Div(id="thumbnail-box", children=
    [
        dbc.Tabs(
            [
                dbc.Tab(all_thumbnails, label="All"),
                dbc.Tab(good_thumbnails, label="Good"),
                dbc.Tab(bad_thumbnails, label="Bad")
            ]
        )
    ]
)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#969696",
    "display": "flex",
    "flex-direction": "column",
    "gap": "1rem"
}

sidebar = html.Div(children=
    [
        filter_box,
        thumbnail_box
    ],
    style=SIDEBAR_STYLE
)

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem"
}

main_picture = html.Div(
    html.P("Picture")
)
    
description = html.Div(children=[
    html.H2("Filename:"),
    html.P("# TODO filename"),
    
    html.H2("Serial #:"),
    html.P("# TODO serialno"),
    
    html.H2("Defect code:"),
    html.P("# TODO defectcode"),
    
    html.H2("Certainty:"),
    html.P("# TODO certainty")
], style = {"background-color": SECONDARY_BG_COLOR})

main_content = html.Div(id="main-content", style=CONTENT_STYLE, children=[
    dbc.Table(
        html.Tbody(
            html.Tr([
                html.Td(main_picture),
                html.Td(description)
            ])
        ),
        bordered = True
    )
])

app.layout = html.Div([dcc.Location(id="url"), sidebar, main_content])

if __name__ == "__main__":
    app.run_server(debug=True)
