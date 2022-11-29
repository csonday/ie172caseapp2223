from dash import html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2("Purchase Orders"),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Purchase Order Management")),
                dbc.CardBody(
                    [
                        dbc.Button('+ Add Purchase Order', color="primary", href='/po/po_profile?mode=add'),
                        html.Hr(),
                        html.Div(
                            [
                                html.H6("Find Records", style={'fontWeight': 'bold'}),
                                dbc.Row(
                                    [
                                        dbc.Label("Search PO ID", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text", id="po_filter_poid", placeholder="Enter filter"
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    "No records to show",
                                    id='po_porecords'
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
        Output('po_porecords', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('po_filter_poid', 'value'), # changing the text box value should update the table
    ]
)
def moviehome_loadpolist(pathname, searchterm):
    if pathname == '/po':
        
        sql = """ SELECT po_id, to_char(po_date, 'DD Mon YYYY')
            FROM po_transactions
            WHERE NOT po_delete_ind
        """
        values = [] 
        cols = ['PO ID', 'Date Created']
        
        
        # Filter
        if searchterm:
            sql += " AND po_id = %s"
            
            values += [searchterm]

        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape: 
            
            # Create the buttons as a list based on the ID
            buttons = []
            for po_id in df['PO ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'po/po_profile?mode=edit&id={po_id}',
                                   size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
            
            df['Action'] = buttons
            
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                    hover=True, size='sm')
            return [table]
        else:
            return ["No records to show"]
        
    else:
        raise PreventUpdate
