import apps.dbconnect as db
from datetime import datetime

def addfewgenres():
    # We use the function modifydatabase() -- it has 2 arguments
    # The first argument is the sql code, where we use a placeholder %s
    # The second argument is ALWAYS a list of values to replace the %s in the sql code
    sqlcode = """ INSERT INTO genres (
        genre_name
    )
    VALUES (%s)"""

    db.modifydatabase(sqlcode, ['Action'])
    db.modifydatabase(sqlcode, ['Horror'])
    # Just some feedback that the code succeeded
    print('done!')
    

sql_resetgenres = """
    TRUNCATE TABLE genres RESTART IDENTITY CASCADE
"""
db.modifydatabase(sql_resetgenres, [])  
addfewgenres()

# querydatafromdatabase(sql, values, dfcolumns)
sql = 'SELECT * FROM genres'
values = []
colnames = ['id', 'name', 'mod_on', 'del_ind']

print(db.querydatafromdatabase(sql, values, colnames))
