from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app

layout = html.Div(
    [
        html.H2("Movies"),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Movie Management")),
                dbc.CardBody(
                    [
                        dbc.Button('Add Movie', color="secondary", href='/movies/movie_profile'),
                        html.Hr(),
                        html.Div(
                            [
                                html.H6("Find Movies", style={'fontWeight': 'bold'}),
                                dbc.Row(
                                    [
                                        dbc.Label("Search Title", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text", id="movie_name_filter", placeholder="Enter filter"
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    "This will contain the table for movies",
                                    id='movie_movielist'
                                )
                            ]
                        )
                    ]
                ),
            ]
        )
    ]
)