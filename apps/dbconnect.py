import psycopg2
import pandas as pd
import os

def getdblocation():
    DATABASE_URL = os.environ['DATABASE_URL']
    db = psycopg2.connect(DATABASE_URL, sslmode='require')
    return db


def modifydatabase(sql, values):
    # used for inserts and updates
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    db.close()
    
    
def querydatafromdatabase(sql, values, dfcolumns):
    # for SELECT commands
    # ARGUMENTS
    # sql -- sql query with placeholders (%s)
    # values -- values for the placeholders
    # dfcolumns -- column names for the output
    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    db.close()
    return rows


def modifydatabasereturnid(sqlcommand, values):
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sqlcommand, values)
    key = cursor.fetchone()[0]
    db.commit()
    db.close()
    return key