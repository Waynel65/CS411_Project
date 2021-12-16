### Useful Resources ###
## https://www.geeksforgeeks.org/python-postgresql-select-data/
## https://www.postgresqltutorial.com/postgresql-python/insert/


import psycopg2     ## postgreSQL module
import json, sys
from final_project import *


## All the insert functions should look similar and all the get functions should be similar to one another

def get_db_connection():
    '''
        establish a DB connection
    '''
    try:
        conn = psycopg2.connect(
            database="users",
            user='postgres',
            password='password',
            #put whatever your postgres password is above^
            host='localhost',
            port= '5432'
        )
        print("connected to database")
        cursor = conn.cursor() 
        return conn, cursor
    except:
        print("connection failed")
        return

def create_table(conn, cursor):
    '''
        creates a table named USERS, which stores
        the userIDs and their relevant info
    '''

    # table explained:
    # ID = index
    # USER_ID = user_name
    # playlist = the id of first playlist
    # music genres = a list stored as a json file
    # book_title = the book recommended
    try:
        sql = '''CREATE TABLE if not exists USERS(
        ID BIGSERIAL NOT NULL,
        USER_ID VARCHAR(100) NOT NULL PRIMARY KEY,
        Playlist VARCHAR(100),
        Music_Genre VARCHAR(100),
        Book_Title VARCHAR(100)
        )'''

        cursor.execute(sql)
        conn.commit()
    except:
        print("The table already exists")
        return


def insert_userID(conn, cursor,userID):
    '''
        This function is used when the user first login to the website
        storing the userID in DB
    '''
    try:
        insert_cmd = "INSERT INTO USERS(USER_ID) VALUES(%s)"
        data = userID
        cursor.execute(insert_cmd, (data,))     ## for some reason the syntax must be like this

        conn.commit()
    except:
        print("This user is already in the database")
    return

def insert_playlist(conn, cursor,userID, playlist):
    '''
        After login, there could a button that invokes this function, which
        fetch the users' playlist from his/her spotify account
        and store the playlist according to his/her userID in DB
    '''
    
    try:
        cmd = "UPDATE USERS SET Playlist=%s where USER_ID=%s"
        cursor.execute(cmd, (playlist, userID), )
        conn.commit()
    except:
        print("playlist existed!")

    return


def insert_music_genre(conn, cursor, userID, music_genre):
    '''
        This function should be invoked after insert_playlist
        This will fetch music_genres present in the playlist and
        insert the results into DB
    '''
    # might need to go through artist to get genre
    try:
        cmd = "UPDATE USERS SET Music_Genre=%s where USER_ID=%s"
        cursor.execute(cmd, (music_genre, userID), )
        conn.commit()
    except:
        print("user has already their fav music genre")

    return

def insert_book_title(userID, book_title):
    '''
        This function should be invoked after fetching books from book API
        and insert the book_title into DB
    '''
    cmd = "UPDATE USERS SET Music_Genre=%s where USER_ID=%s"
    cursor.execute(cmd, (book_title, userID), )
    conn.commit()

    return 


def get_user_playlist(conn, cursor, userID):
    '''
        this function retrieves the playlist json file from DB
        according to the related userID
    '''
    query = "SELECT Playlist FROM USERS where USER_ID=%s"
    cursor.execute(query, (userID,))
    result = cursor.fetchall()
    print(result)
    return result[0][0]


def get_user_music_genre(conn, cursor,userID):
    '''
        this function retrieves the music_genre from DB
        according to the related userID
    '''
    query = "SELECT Music_Genre FROM USERS where USER_ID=%s"
    cursor.execute(query, (userID,))
    result = cursor.fetchall()
    # print("result" , result[0][0])
    return result[0][0]

def get_user_book_title(userID):
    '''
        this function retrieves the book_title from DB
        according to the related userID
    '''
    query = "SELECT Book_Title FROM USERS where USER_ID=%s"
    cursor.execute(query, (userID,))
    result = cursor.fetchall()
    print(result)

    return result[0][0]

def user_exist(conn, cursor, userID):
    '''
        check if user has all relevant info stored in DB
    '''

    try:
        check_userID = "SELECT USER_ID FROM USERS where USER_ID=%s"
        cursor.execute(check_userID, (userID,))
        
        check_playlist = "SELECT Playlist FROM USERS where USER_ID=%s"
        cursor.execute(check_playlist, (userID,))

        check_music_genre = "SELECT Music_Genre FROM USERS where USER_ID=%s"
        cursor.execute(check_music_genre, (userID,))

        check_book_title = "SELECT Book_Title FROM USERS where USER_ID=%s"
        cursor.execute(check_book_title, (userID,))
        return True

    except:
        
        return False

def view_table():
    '''
        view data currently stored in table
    '''
    cursor.execute("SELECT * FROM USERS")
    print(cursor.fetchall())

    conn.commit()
    return

#TODO: why is this not working
def read_json_file(json_path):
    '''
        for testing purposes: used for parsing local json file
    '''
    with open(json_path) as json_file:
        json_data = json.load(json_file)
        # print(type(json_data))
        # print(type(json.dumps(json_data)))
        return json_data

## testing ##

# def get_USERID():
#     query = "SELECT USER_ID FROM USERS where ID=1"
#     cursor.execute(query)
#     result = cursor.fetchall()
#     print(result)
#     return

### MAIN FUNCTION ###
if __name__ == "__main__":

    # establishing the connection
    try:
        conn = psycopg2.connect(
            database="users",
            user='postgres',
            password='1Eden2Hui',
            #put whatever your postgres password is above^
            host='localhost',
            port= '5432'
        )

        cursor = conn.cursor()  ## creating a cursor object (basically a handler for SQL code)
    except:
        print("CONNECTION FAILED")
    
    create_table()
    # insert_userID('XXX')
    # playlist_test = read_json_file("samplePlaylistResponse.json")
    # insert_playlist('XXX', playlist_test)
    #insert_playlist("wayne", "test")
    #view_table()
    #get_user_playlist("wayne")

    #insert_userID("Bob")
    #insert_music_genre("Bob", "test")
    #insert_book_titles("Bob", "test")
    #get_user_music_genre("Bob")
    #get_user_book_titles("Bob")
    
    if conn is not None:
        conn.close()
    
