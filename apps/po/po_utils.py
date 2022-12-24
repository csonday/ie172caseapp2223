# This file contains the functions used in po_profile.py
from apps import dbconnect as db
from dash import html
import dash_bootstrap_components as dbc


def getItemDropdown(mode='add', po_id=0, po_item_id=None):
    sql = """ SELECT item_id as value,
        item_name as label
    FROM items
    WHERE
        TRUE
    """
    # we put true so we can add additional constraints below
    val = []
    
    if mode == 'add' and not po_id:
        # if po is not yet in db
        pass
    
    elif mode == 'add' and po_id:
        # if po already in db
        # exclude the items already in the PO
        
        sql += """ AND item_id NOT IN (
            SELECT item_id 
            FROM po_items 
            WHERE po_id = %s
                AND NOT po_item_delete_ind
        )"""
        val += [po_id]
        
    else:
        # if edit mode, add the current item_id in the options
        # so it appears on the dropdown
        sql += """ AND item_id NOT IN (
            SELECT item_id 
            FROM po_items 
            WHERE po_id = %s
                AND po_item_id <> %s
                AND NOT po_item_delete_ind
        )"""
        val += [po_id, po_item_id]
    
    df = db.querydatafromdatabase(sql, val, ['value', 'label'])
    
    return df.to_dict('records')


def converttoint(num):
    try:
        num = int(num)
        if num > 0:
            return num
        else:
            return 0
    except:
        return 0
    

def createPOrecord(date, remarks):
    sql = """INSERT INTO po_transactions(po_date, po_remarks)
    VALUES (%s, %s) 
    RETURNING po_id"""
    values = [date, remarks]
    
    po_id = db.modifydatabasereturnid(sql, values)
    
    return po_id


def managePOLineItem(poid, newline):
    
    # note that the table has restrictions 
    # on having unique(po_id, item_id).
    # If we insert a duplicate row, this sql command 
    # updates the existing record instead.
    sql = """INSERT INTO po_items(po_id, item_id, po_item_qty)
    VALUES (%(poid)s, %(itemid)s, %(qty)s) 
    ON CONFLICT (po_id, item_id) DO 
    UPDATE 
        SET 
            po_item_delete_ind = false,
            po_item_qty = %(qty)s"""
    values = {
        'poid': poid,
        'itemid': newline['itemid'],
        'qty': newline['itemqty']
    }
    db.modifydatabase(sql, values)
    
    
def removeLineItem(po_item_id):
    sql = """UPDATE po_items
    SET po_item_delete_ind = true
    WHERE po_item_id = %s"""
    
    val = [po_item_id]
    db.modifydatabase(sql, val)
    

def queryPOLineItems(po_id):
    sql = """SELECT
        item_name,
        po_item_qty,
        po_item_id
    FROM po_items pi
        INNER JOIN items i ON i.item_id = pi.item_id
    WHERE 
        NOT po_item_delete_ind AND
        po_id = %s
    """
    val = [po_id]
    cols = ['Item', 'Qty', 'id']
    
    return db.querydatafromdatabase(sql, val, cols)


def formatPOtable(df):
    # align numbers to the right
    df['Qty'] = df['Qty'].apply(lambda num: html.Div(f"{num:,.2f}", className='text-right'))
            
    # add the Edit buttons
    buttons = []
    for id in df['id']:
        buttons += [
            html.Div(
                dbc.Button('Edit', id={'index':id, 'type': 'poprof_editlinebtn'},
                            size='sm', color='warning'),
                style={'text-align': 'center'}
            )
        ]
    
    df['Action'] = buttons
    
    # add an item# column
    df.insert(
        loc=0, 
        column='Item #', 
        value=[html.Div(i+1, className='text-center') for i in range(len(df.index))]
    )
    
    # remove the id column
    df.drop('id', axis=1, inplace=True)
    
    return dbc.Table.from_dataframe(df, striped=True, bordered=True,
            hover=True, size='sm')
    
    
def getPOLineData(lineid):
    sql = """SELECT
        item_id,
        po_item_qty
    FROM po_items pi
    WHERE 
        po_item_id = %s
    """
    val = [lineid]
    cols = ['item', 'qty']
    
    df = db.querydatafromdatabase(sql, val, cols)
    
    return [df[i][0] for i in cols]


def checkPOLineItems(po_id):
    sql = """SELECT COUNT(*)
    FROM po_items
    WHERE NOT po_item_delete_ind
        AND po_id = %s"""
    val = [po_id]
    col = ['count']
    
    df = db.querydatafromdatabase(sql, val, col)
    
    return df['count'][0]


def deletePO(po_id):
    sql = """UPDATE po_transactions
    SET po_delete_ind = true
    WHERE po_id = %s"""
    
    val = [po_id]
    db.modifydatabase(sql, val)