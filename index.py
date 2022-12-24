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
from apps import login, signup

CONTENT_STYLE = {
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

app.layout = html.Div(
    [
        # Location Variable -- contains details about the url
        dcc.Location(id='url', refresh=True),
        
        
        # LOGIN DATA
        # 1) logout indicator, storage_type='session' means that data will be retained
        #  until browser/tab is closed (vs clearing data upon refresh)
        dcc.Store(id='sessionlogout', data=False, storage_type='session'),
        
        # 2) current_user_id -- stores user_id
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        
        # 3) currentrole -- stores the role
        # we will not use them but if you have roles, you can use it
        dcc.Store(id='currentrole', data=-1, storage_type='session'),
        
        html.Div(
            cm.navbar,
            id='navbar_div'
        ),
        
        # Page Content -- Div that contains page layout
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)


# if the URL changes, the content changes as well
@app.callback(
    [
        Output('page-content', 'children'),
        Output('navbar_div', 'style'),
        Output('sessionlogout', 'data'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
    ]
)
def displaypage(pathname, sessionlogout, currentuserid):
    
    # determines what element triggered the function
    ctx = dash.callback_context
    if ctx.triggered:
        # eventid = name of the element that caused the trigger
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
    
    if eventid == 'url':
        print(currentuserid, pathname)
        if currentuserid < 0:
            if pathname in ['/']:
                returnlayout = login.layout
            elif pathname == '/signup':
                returnlayout = signup.layout
            else:
                returnlayout = '404: request not found'
            
        else:
            if pathname == '/logout':
                returnlayout = login.layout
                sessionlogout = True
                
            elif pathname in ['/', '/home']:
                returnlayout = home.layout
                
            elif pathname == '/movies':
                returnlayout = movies_home.layout
            elif pathname == '/movies/movie_profile':
                returnlayout = movie_profile.layout
            
            
            elif pathname == '/genres':
                returnlayout = "i like horror"
                
            else:
                returnlayout = '404: request not found'
    else:
        raise PreventUpdate
    
    navbar_div = {'display':  'none' if sessionlogout else 'unset'}
    return [returnlayout, navbar_div, sessionlogout]



if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)