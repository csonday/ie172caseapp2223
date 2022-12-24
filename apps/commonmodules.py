from dash import html
import dash_bootstrap_components as dbc

navlink_style = {
    'color': '#fff'
}

navbar = dbc.Navbar(
    [
        html.A(
            dbc.NavbarBrand("IE 172 Case App", className="ml-2", 
                            style={'margin-right': '2em'}),
            href="/home",
        ),
        dbc.NavLink("Home", href="/home", style=navlink_style),
        dbc.NavLink("Movies", href="/movies", style=navlink_style),
        dbc.NavLink("Genres", href="/genres", style=navlink_style),
        dbc.NavLink("Purchase Orders", href="/po", style=navlink_style),
        dbc.NavLink("Logout", href="/logout", style=navlink_style),
    ],
    dark=True,
    color='dark'
)