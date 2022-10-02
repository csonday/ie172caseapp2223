from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import webbrowser

from app import app
from apps import commonmodules as cm
from apps import home
from apps.movies import movies_home, movie_profile


CONTENT_STYLE = {
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

app.layout = html.Div(
    [
        # Location Variable -- contains details about the url
        dcc.Location(id='url', refresh=True),
        cm.navbar,
        # Page Content -- Div that contains page layout
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)


# if the URL changes, the content changes as well
@app.callback(
    [
        Output('page-content', 'children')
    ],
    [
        Input('url', 'pathname'),
    ]
)
def displaypage(pathname):
    
    # determines what element triggered the function
    ctx = dash.callback_context
    if ctx.triggered:
        # eventid = name of the element that caused the trigger
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
    
    if eventid == 'url':
        if pathname in ['/', '/home']:
            returnlayout = home.layout
            
            
        elif pathname == '/movies':
            returnlayout = movies_home.layout
        elif pathname == '/movies/movie_profile':
            returnlayout = movie_profile.layout
        
        
        elif pathname == '/genres':
            returnlayout = "i like horror"
            
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    
    return [returnlayout]



if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)