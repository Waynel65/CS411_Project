### Useful Resources ###
## https://www.geeksforgeeks.org/python-postgresql-select-data/
## https://www.postgresqltutorial.com/postgresql-python/insert/


import psycopg2     ## postgreSQL module
from final_project import *


#TODO: 
# also still need to decide what format are we storing the playlist and other stuff in (json or smth else)

def create_table():
    '''
        creates a table named USERS, which stores
        the userIDs and their relevant info
    '''

    try:
        sql = '''CREATE TABLE USERS(
        ID BIGSERIAL NOT NULL PRIMARY KEY,
        USER_ID VARCHAR(100) NOT NULL,
        Playlist jsonb,
        Music_Genre jsonb,
        Book_Titles jsonb
        )'''

        cursor.execute(sql)
        conn.commit()
    except:
        print("The table already exists")
        return

def insert_userID(userID):
    '''
        This function is used when the user first login to the website
        storing the userID in DB
    '''
    insert_cmd = "INSERT INTO USERS(USER_ID) VALUES(%s)"
    data = userID
    cursor.execute(insert_cmd, (data,))     ## for some reason the syntax must be like this

    conn.commit()
    return

def insert_playlist(userID, playlist):
    '''
        After login, there could a button that invokes this function, which
        fetch the users' playlist from his/her spotify account
        and store the playlist according to his/her userID in DB
    '''

    return

def insert_music_genre(userID, music_genre):
    '''
        This function should be invoked after insert_playlist
        This will fetch music_genres present in the playlist and
        insert the results into DB
    '''
    return

def insert_book_titles(userID, book_titles):
    '''
        This function should be invoked after fetching books from book API
        and insert the book_titles into DB
    '''
    return 

def view_table():
    '''
        view data currently stored in table
    '''
    cursor.execute("SELECT * FROM USERS")
    print(cursor.fetchall())

    conn.commit()
    return

## testing ##
def get_USERID():
    query = "SELECT USER_ID FROM USERS where ID=1"
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    return

### MAIN FUNCTION ###
if __name__ == "__main__":

    # establishing the connection
    try:
        conn = psycopg2.connect(
            database="users",
            user='postgres',
            password='password',
            host='localhost',
            port= '5432'
        )

        cursor = conn.cursor()  ## creating a cursor object (basically a handler for SQL code)
    except:
        print("CONNECTION FAILED")
    
    # view_table()
    # get_USERID()
    
    if conn is not None:
        conn.close()
    