from dash import html

layout = html.Div(
    [
    html.H2('Welcome to our app!'),
    html.Hr(),
    html.Div(
        [
            html.Span(
                "Thru this app, you can manage a database of movies that are classified according to genres.",
            ),
            html.Br(),
            html.Br(),
            html.Span(
                "Contact the owner if you need assistance!",
                style={'font-style':'italic'}
            ),
        ]
        )
    ]
)