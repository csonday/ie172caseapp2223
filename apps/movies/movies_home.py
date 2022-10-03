from logging import warning
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
        Output('movie_movielist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('movie_name_filter', 'value'),
    ]
)
def updatemovielist(pathname, searchterm):
    if pathname == '/movies':
        # 1. query the relevant records
        sql = """SELECT movie_name, genre_name, movie_id
                FROM movies m
                    INNER JOIN genres g ON m.genre_id = g.genre_id
                WHERE NOT movie_delete_ind"""
        val = []
        colnames = ['Movie Title', 'Genre', 'ID']
        
        if searchterm:
            sql += """ AND movie_name ILIKE %s"""
            val += [f"%{searchterm}%"]
        
        
        movies = db.querydatafromdatabase(sql, val, colnames)
        
        # 2. create the table and add it to the interface
        
        if movies.shape[0]:
            # add the buttons with the respective href
            buttons = []
            for movieid in movies['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit/Delete', href=f"/movies/movie_profile?mode=edit&id={movieid}",
                               size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
            
            # we add the buttons to the movies table
            movies['Action'] = buttons
            
            # remove the ID column
            movies.drop('ID', axis=1, inplace=True)
            
            table = dbc.Table.from_dataframe(movies, striped=True, bordered=True, hover=True, size='sm')
            
            return [table]
        else:
            return ["There are no records that match the search term."]
        
    else:
        raise PreventUpdate