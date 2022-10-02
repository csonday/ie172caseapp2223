from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2("Movies"),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Movie Management")),
                dbc.CardBody(
                    [
                        dbc.Button('Add Movie', color="secondary", href='/movies/movie_profile?mode=add'),
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


@app.callback(
    [
        Output('movie_movielist', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('movie_name_filter', 'value'), # changing the text box value should update the table
    ]
)
def moviehome_loadmovielist(pathname, searchterm):
    if pathname == '/movies':
        # 1. Obtain records from the DB via SQL
        # 2. Create the html element to return to the Div
        sql = """ SELECT movie_name, genre_name
            FROM movies m
                INNER JOIN genres g ON m.genre_id = g.genre_id
            WHERE 
                NOT movie_delete_ind
        """
        values = [] # blank since I do not have placeholders in my SQL
        cols = ['Movie Title', 'Genre']
        
        
        ### ADD THIS IF BLOCK
        if searchterm:
            # We use the operator ILIKE for pattern-matching
            sql += " AND movie_name ILIKE %s"
            
            # The % before and after the term means that
            # there can be text before and after
            # the search term
            values += [f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape: # check if query returned anything
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                    hover=True, size='sm')
            return [table]
        else:
            return ["No records to display"]
        
    else:
        raise PreventUpdate
