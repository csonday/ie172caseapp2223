from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
from urllib.parse import urlparse, parse_qs
from datetime import date
import json

from app import app
from apps import dbconnect as db
from apps.po import po_utils as util

layout = html.Div(
    [
        html.Div( # This div shall contain all dcc.Store objects
            [
                dcc.Store(id='poprof_toload', storage_type='memory', data=0),
                dcc.Store(id='poprof_poid', storage_type='memory', data=0),
                dcc.Store(id='poprof_linetoedit', storage_type='memory', data=0),
            ]
        ),

        html.H2("PO Details"),
        html.Hr(),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Label("Transaction Date", width=2),
                        dbc.Col(
                            dcc.DatePickerSingle(
                                id='poprof_transactiondate',
                                date=date.today()
                            ),
                            width=6,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("PO Remarks", width=2),
                        dbc.Col(
                            dbc.Textarea(
                                className="mb-3",
                                placeholder="Add remarks",
                                id='poprof_remarks'
                            ),
                            width=6,
                        ),
                    ],
                    className="mb-3",
                ),
            ]    
        ),
        html.Hr(),
        
        # We don't need a div here but I like using one
        # to signify a new section
        html.Div(
            [
                dbc.Alert("Please fill out the information above before proceeding", id='poprof_alertmissingdata',
                          color='danger', is_open=False),
                dbc.Button("Add Line Item", id="poprof_addlinebtn", 
                           color='primary', n_clicks=0,
                           style={'display':'inline-block','border-radius':'5px'}
                ),  
                html.Br(),
                html.Br(),
                html.Div(
                    # This will contain the table of line items
                    id='poprof_lineitems'
                )
            ]    
        ),
        
        dbc.Modal(
            [
                dbc.ModalHeader("Add Line Item", id='poprof_linemodalhead'),
                dbc.ModalBody(
                    [
                        dbc.Alert(id='poprof_linealert', color='warning', is_open=False),
                        dbc.Row(
                            [
                                dbc.Label("Item", width=4),
                                dbc.Col(
                                    html.Div(
                                        dcc.Dropdown(
                                            id='poprof_lineitem',
                                            clearable=True,
                                            searchable=True,
                                            options=[]
                                        ), 
                                        className="dash-bootstrap"
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Qty", width=4),
                                dbc.Col(
                                    dbc.Input(
                                        type="number", id="poprof_lineqty", placeholder="Enter qty"
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=4),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='poprof_lineremove',
                                            options=[
                                                {
                                                    'label': "Mark for Deletion",
                                                    'value': 1
                                                }
                                            ],
                                            # I want the label to be bold
                                            style={'fontWeight':'bold'}, 
                                        ),
                                        width=6,
                                        style={'margin': 'auto 0'}
                                    ),
                                ],
                                className="mb-3",
                            ),
                            id='poprof_lineremove_div'
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    [
                        html.Div(
                            [
                                dbc.Button('Cancel', id='poprof_cancellinebtn', color='secondary'),
                                dbc.Button('Save Line Item', id='poprof_savelinebtn', color='primary'),
                            ],
                            # these are to separate the buttons to opposite ends
                            className='d-flex justify-content-between',
                            style={'flex': '1'}
                        )
                    ]
                )
            ],
            id='poprof_modal',
            backdrop='static',
            centered=True
        ),
        
        # enclosing the checklist in a Div so we can
        # hide it in Add Mode
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Wish to delete?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='poprof_removerecord',
                            options=[
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1
                                }
                            ],
                            # I want the label to be bold
                            style={'fontWeight':'bold'}, 
                        ),
                        width=6,
                        style={'margin': 'auto 0'}
                    ),
                ],
                className="mb-3",
            ),
            id='poprof_removerecord_div'
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Trying to leave the page...")),
                dbc.ModalBody("tempmessage", id='poprof_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="poprof_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="poprof_modalsubmitted",
            is_open=False,
        ),
        html.Hr(),
        
        html.Div(
            [
                dbc.Button('Cancel', id='poprof_cancelbtn', color='secondary'),
                dbc.Button('Submit', color="primary", id='poprof_savebtn'),
            ],
            # these are to separate the buttons to opposite ends
            className='d-flex justify-content-between',
            style={'flex': '1'}
        )
    ]
)

@app.callback(
    [
        Output('poprof_toload', 'data'),
        # we want to update the style of this element
        Output('poprof_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search') 
    ]
)
def pageLoadOperations(pathname, search):
    
    if pathname == '/po/po_profile':
                
        # are we on add or edit mode?
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        
        # to show the remove option?

        removediv_style = {'display': 'none'} if not to_load else None
        # if to_load = 0, then not to_load -> not 0 -> not False -> True
    
    else:
        raise PreventUpdate

    return [to_load, removediv_style]


@app.callback(
    [
        Output('poprof_transactiondate', 'date'),
        Output('poprof_remarks', 'value'),
    ],
    [
        Input('poprof_toload', 'modified_timestamp'),
        # toload is a dcc.store element. To use them in Input(), 
        # property should be 'modified_timestamp'
    ],
    [
        State('poprof_toload', 'data'),
        State('url', 'search') 
    ]
)
def populatePOData(timestamp, toload, search):
    if toload == 1:
        
        parsed = urlparse(search)
        po_id = int(parse_qs(parsed.query)['id'][0])
        
        sql = """SELECT po_date, po_remarks
        FROM po_transactions
        WHERE po_id = %s"""
        val = [po_id]
        col = ['date', 'remarks']
        
        df = db.querydatafromdatabase(sql, val, col)
        
        transactiondate, remarks = [df[i][0] for i in col]
        
    else:
        raise PreventUpdate
    
    return [transactiondate, remarks]


@app.callback(
    [
        Output('poprof_modal', 'is_open'),
        Output('poprof_alertmissingdata', 'is_open'),
        Output('poprof_lineremove_div', 'className'),
        Output('poprof_poid', 'data'),
        
        Output('poprof_lineitem', 'options'),
        Output('poprof_linealert', 'children'),
        Output('poprof_linealert', 'is_open'),
        Output('poprof_linetoedit', 'data'),
        
        Output('poprof_lineitems', 'children'),
        Output('poprof_linemodalhead', 'children'),
        Output('poprof_savelinebtn', 'children'),
    ],
    [
        Input('poprof_addlinebtn', 'n_clicks'),
        Input('poprof_savelinebtn', 'n_clicks'),
        Input('poprof_cancellinebtn', 'n_clicks'),
        Input({'index': ALL, 'type': 'poprof_editlinebtn'}, 'n_clicks'),
        
        Input('poprof_toload', 'modified_timestamp'),
        
    ],
    [
        State('url', 'search'),
        State('poprof_transactiondate', 'date'),
        State('poprof_remarks', 'value'),
        State('poprof_poid', 'data'),
        
        State('poprof_lineitem', 'options'),
        State('poprof_lineitem', 'value'),
        State('poprof_lineqty', 'value'),
        State('poprof_linetoedit', 'data'),
        
        State('poprof_lineremove', 'value'),
        State('poprof_lineitems', 'children'),
        State('poprof_toload', 'data'),
        State('poprof_linemodalhead', 'children'),
        
        State('poprof_savelinebtn', 'children'),
    ]
)
def toggleModal(addlinebtn, savebtn, cancelbtn, editlinebtn,
                toload_timestamp,
                
                search, transactiondate, remarks, po_id,
                item_options, itemid, itemqty, linetoedit,
                removeitem, linetable, toload, linemodalhead,
                addlinebtntxt):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        parsed = urlparse(search)
        
        # some default values
        openmodal = False
        openalert_missingdata = False
        lineremove_class = 'd-none' # hide the remove tickbox
        
        linealert_message = ''
        updatetable = False # for updating table of line items
    else:
        raise PreventUpdate
    
    PO_requireddata = [
        transactiondate, 
        remarks
    ]
    
    if eventid == 'poprof_addlinebtn' and addlinebtn and all(PO_requireddata):
        openmodal = True
        item_options = util.getItemDropdown('add', po_id)
        linetoedit = 0
        
        # Edit modal text (buttons, headers)
        linemodalhead = 'Add Line Item'
        addlinebtntxt = 'Save Line Item'
    
    elif eventid == 'poprof_addlinebtn' and addlinebtn and not all(PO_requireddata):
        openalert_missingdata = True
        
    elif eventid == 'poprof_cancellinebtn' and cancelbtn:
        pass
    
    elif 'poprof_editlinebtn' in eventid and any(editlinebtn):
        # if any of the buttons for editing si clicked
        
        openmodal = True
        lineremove_class = '' # show line remove option
        linetoedit = int(json.loads(eventid)['index'])
        item_options = util.getItemDropdown('edit', po_id)
        
        # Edit modal text (buttons, headers)
        linemodalhead = 'Edit Line Item'
        addlinebtntxt = 'Update Line Item'
        
    elif eventid == 'poprof_toload' and toload == 1:
        updatetable = True
        po_id = int(parse_qs(parsed.query)['id'][0])
    
        
    elif eventid == 'poprof_savelinebtn' and savebtn:
        # validate inputs
        inputs = [
            itemid, 
            util.converttoint(itemqty)>0
        ]
        
        if not all(inputs):
            linealert_message = "Please ensure that fields are filled in and inputs are correct."
        
        else:
            # proceed to saving the line item
            
            newline = {
                'itemid': itemid,
                'itemqty': int(itemqty),
            }
            
            # if add mode:
            if linetoedit == 0:
                # if PO record not yet in db, save PO first
                if not po_id:
                    po_id = util.createPOrecord(transactiondate, remarks)
                
                util.managePOLineItem(po_id, newline)
            
            else:
                if removeitem:
                    util.removeLineItem(linetoedit)
                else:
                    util.managePOLineItem(po_id, newline)
            
            updatetable = True
    
    else:
        raise PreventUpdate
    
    
    if updatetable:
        df = util.queryPOLineItems(po_id)
        
        if df.shape[0]:
            linetable = util.formatPOtable(df)
        else:
            linetable = html.Div('No records to display', style={'color':'#777', 'padding-left': '2em'})

    # if we have an error prompt, linealert should open
    openalert_linealert = bool(linealert_message)
    
    return [
        openmodal, 
        openalert_missingdata, 
        lineremove_class,
        po_id,
        
        item_options,
        linealert_message,
        openalert_linealert,
        linetoedit,
        
        linetable,
        linemodalhead,
        addlinebtntxt
    ]


@app.callback(
    [
        Output('poprof_lineitem', 'value'),
        Output('poprof_lineqty', 'value'),
        Output('poprof_lineremove', 'value'),
    ],
    [
        Input('poprof_addlinebtn', 'n_clicks'),
        Input('poprof_linetoedit', 'modified_timestamp'),
    ],
    [
        State('poprof_linetoedit', 'data'),
        State('poprof_lineitem', 'value'),
        State('poprof_lineqty', 'value'),
        State('poprof_lineremove', 'value'),
    ]
)
def clearFields(addlinebtn, line_timestamp, 
                
                linetoedit, itemid, itemqty, removeitem):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
    
    
    if eventid == 'poprof_addlinebtn' and addlinebtn:
        itemid, itemqty = None, None
        removeitem = []
        
    elif eventid == 'poprof_linetoedit' and linetoedit:
        itemid, itemqty = util.getPOLineData(linetoedit)
        removeitem = []
        
    else:
        raise PreventUpdate
    
    return [itemid, itemqty, removeitem]


@app.callback(
    [
        Output('poprof_modalsubmitted', 'is_open'),
        Output('poprof_feedback_message', 'children'),
        Output('poprof_closebtn', 'href'),
    ],
    [
        Input('poprof_savebtn', 'n_clicks'),
        Input('poprof_cancelbtn', 'n_clicks'),
        Input('poprof_closebtn', 'n_clicks'),
    ],
    [
        State('poprof_poid', 'data'),
        State('poprof_removerecord', 'value'),
        State('poprof_toload', 'data') 
    ]
)
def finishTransaction(submitbtn, cancelbtn, closebtn,
                      
                      po_id, removerecord, iseditmode):
    ctx = dash.callback_context
    if ctx.triggered:
        # eventid = name of the element that caused the trigger
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate
    
    if eventid == 'poprof_savebtn' and submitbtn:
        openmodal = True
        
        # check if we have line items
        if not po_id:
            feedbackmessage = "You have not filled out the form."
            
        elif not util.checkPOLineItems(po_id):
            feedbackmessage = "Please add line items"
            
        elif removerecord:
            util.deletePO(po_id)
            feedbackmessage = "Record has been deleted. Click OK to go back to PO Home."
            okay_href = '/po'
            
        else:
            feedbackmessage = "PO is saved. Click OK to go back to PO Home."
            okay_href = '/po'
            
    elif eventid == 'poprof_cancelbtn' and cancelbtn:
        openmodal = True
        
        if not po_id:
            feedbackmessage = "Click OK to go back to PO Home."
            okay_href = '/po'
        elif iseditmode and po_id:
            feedbackmessage = "Changes have been discarded. Click OK to go back to PO Home."
            okay_href = '/po'
        else:
            feedbackmessage = "Click OK to go back to PO Home."
            okay_href = '/po'
            
    
    elif eventid == 'poprof_closebtn' and closebtn:
        pass
    
    else:
        raise PreventUpdate
    
    return [openmodal, feedbackmessage, okay_href]
