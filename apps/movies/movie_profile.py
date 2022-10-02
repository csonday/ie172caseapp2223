from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from urllib.parse import urlparse, parse_qs

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2("Movie Details"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Title", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="movieprof_title", placeholder="Enter filter"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Release Date", width=2),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='movieprof_releasedate'
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Genre", width=2),
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                            id='movieprof_genre',
                            clearable=True,
                            searchable=True,
                        ), 
                        className="dash-bootstrap"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        html.Hr(),
        dbc.Button('Submit', color="secondary", id='moviesprof_submitbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage", id='movieprof_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="movieprof_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="movieprof_modal",
            is_open=False,
        ),
    ]
)

@app.callback(
    [
        Output('movieprof_genre', 'options'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def movieprof_loaddropdown(pathname):
    
    if pathname == '/movies/movie_profile':
        sql = """
            SELECT genre_name as label, genre_id as value
            FROM genres
            WHERE genre_delete_ind = False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        genre_opts = df.to_dict('records')
    
    else:
        raise PreventUpdate

    return [genre_opts]


@app.callback(
    [
        Output('movieprof_modal', 'is_open'),
        Output('movieprof_feedback_message', 'children'),
        Output('movieprof_closebtn', 'href'),
    ],
    [
        Input('moviesprof_submitbtn', 'n_clicks'),
        Input('movieprof_closebtn', 'n_clicks'),
    ],
    [
        State('movieprof_title', 'value'),
        State('movieprof_releasedate', 'date'),
        State('movieprof_genre', 'value'),
        State('url', 'search'), # we need this to identify which mode we are in
    ]
)
def movieprof_submitprocess(submitbtn, closebtn,
                            
                            title, releasedate, genre,
                            search):
    ctx = dash.callback_context
    if ctx.triggered:
        # eventid = name of the element that caused the trigger
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate
    
    if eventid == 'moviesprof_submitbtn' and submitbtn:
        openmodal = True
        
        # check if you have inputs
        inputs = [
            title, 
            releasedate,
            genre
        ]
        
        # if erroneous inputs, raise prompt
        if not all(inputs):
            feedbackmessage = "Please supply all inputs."
        elif len(title)>256:
            feedbackmessage = "Title is too long (length>256)."
        
        # else, save to db and have feedback
        else:
            # parse or decode the 'mode' portion of the search queries 
            parsed = urlparse(search)
            create_mode = parse_qs(parsed.query)['mode'][0]
            
            if create_mode == 'add':
                # save to db
                sqlcode = """INSERT INTO movies(
                    movie_name,
                    genre_id,
                    movie_release_date,
                    movie_delete_ind
                )
                VALUES (%s, %s, %s, %s)
                """
                values = [title, genre, releasedate, False]
                db.modifydatabase(sqlcode, values)
                
                feedbackmessage = "Movie has been saved."
                okay_href = '/movies'
            
            elif create_mode == 'edit':
                # we define this later
                pass
            
            else:
                # if mode value is unidentifiable
                raise PreventUpdate
    
    elif eventid == 'movieprof_closebtn' and closebtn:
        pass
    
    else:
        raise PreventUpdate
    
    return [openmodal, feedbackmessage, okay_href]