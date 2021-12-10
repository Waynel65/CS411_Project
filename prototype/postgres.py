### Useful Resources ###
## https://www.geeksforgeeks.org/python-postgresql-select-data/
## https://www.postgresqltutorial.com/postgresql-python/insert/


import psycopg2     ## postgreSQL module
from final_project import *

# establishing the connection
try:
    conn = psycopg2.connect(
        database="users",
        user='postgres',
        password='password',
        host='localhost',
        port= '5432'
    )

    ## creating a cursor object (basically a handler for SQL code)
    cursor = conn.cursor()
except:
    print("connection failed")

## Create Table (TableName = USERS)
#TODO: still need to find a way to not create table multiple times #
# currently, if one tries to create table when the table is already created, everything breaks
# also still need to decide what format are we storing the playlist and other stuff in (json or smth else)

try:
    sql = '''CREATE TABLE USERS(
    ID BIGSERIAL NOT NULL PRIMARY KEY,
    USER_ID VARCHAR(100) NOT NULL,
    Playlist jsonb,
    Music_Genre jsonb,
    Book_Titles jsonb
    )'''

    cursor.execute(sql)
except:
    print("The table already exists")


## testing insertion into table
insert_cmd = "INSERT INTO USERS(USER_ID) VALUES(%s)"

data = 'UserX'
cursor.execute(insert_cmd, (data,))     ## for some reason the syntax must be like this

## view table
cursor.execute("SELECT * FROM USERS")
print(cursor.fetchall())


conn.commit()

conn.close()