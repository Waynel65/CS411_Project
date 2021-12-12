### Useful Resources ###
## https://www.geeksforgeeks.org/python-postgresql-select-data/
## https://www.postgresqltutorial.com/postgresql-python/insert/


import psycopg2     ## postgreSQL module
import json, sys
from final_project import *


## All the insert functions should look similar and all the get functions should be similar to one another

def create_table():
    '''
        creates a table named USERS, which stores
        the userIDs and their relevant info
    '''

    try:
        sql = '''CREATE TABLE if not exists USERS(
        ID BIGSERIAL NOT NULL,
        USER_ID VARCHAR(100) NOT NULL PRIMARY KEY,
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
    try:
        insert_cmd = "INSERT INTO USERS(USER_ID) VALUES(%s)"
        data = userID
        cursor.execute(insert_cmd, (data,))     ## for some reason the syntax must be like this

        conn.commit()
    except:
        print("This user is already in the database")
    return

def insert_playlist(userID, playlist):
    '''
        After login, there could a button that invokes this function, which
        fetch the users' playlist from his/her spotify account
        and store the playlist according to his/her userID in DB
    '''
    ##TODO: !!! this part needs to be changed to retrieving json from API after Justin set up OAuth
    #If there's an error where it says that it can't find the JSON file, might need to specify path
    with open("./huishi/Desktop/CS411_Project-main/prototype/samplePlaylistResponse.json") as playlist_file:
        playlist_data = json.load(playlist_file)
        cmd = "UPDATE USERS SET Playlist=%s where USER_ID=%s"
        cursor.execute(cmd, (json.dumps(playlist_data), userID), )
    conn.commit()

    return


#Hui
##TODO: finish this function
def insert_music_genre(userID, music_genre):
    '''
        This function should be invoked after insert_playlist
        This will fetch music_genres present in the playlist and
        insert the results into DB
    '''
    # might need to go through artist to get genre
    with open("./huishi/Desktop/CS411_Project-main/samplePlaylistResponse.json") as genre_file:
        genre_data = json.load(genre_file)
        cmd = "UPDATE USERS SET Music_Genre=%s where USER_ID=%s"
        cursor.execute(cmd, (json.dumps(genre_data), userID), )
    conn.commit()

    return

##TODO: finish this function
def insert_book_titles(userID, book_titles):
    '''
        This function should be invoked after fetching books from book API
        and insert the book_titles into DB
    '''
    with open("./huishi/Desktop/CS411_Project-main/samplePlaylistResponse.json") as book_file:
        book_data = json.load(book_file)
        cmd = "UPDATE USERS SET Music_Genre=%s where USER_ID=%s"
        cursor.execute(cmd, (json.dumps(book_data), userID), )
    conn.commit()

    return 


def get_user_playlist(userID):
    '''
        this function retrieves the playlist json file from DB
        according to the related userID
    '''
    query = "SELECT Playlist FROM USERS where USER_ID=%s"
    cursor.execute(query, (userID,))
    result = cursor.fetchall()
    print(result)
    return

##TODO: finish this function
def get_user_music_genre(userID):
    '''
        this function retrieves the music_genre json file from DB
        according to the related userID
    '''
    query = "SELECT Music_Genre FROM USERS where USER_ID=%s"
    cursor.execute(query, (userID,))
    result = cursor.fetchall()
    print(result)
    return

##TODO: finish this function
def get_user_book_titles(userID):
    '''
        this function retrieves the book_titles json file from DB
        according to the related userID
    '''
    query = "SELECT Book_Titles FROM USERS where USER_ID=%s"
    cursor.execute(query, (userID,))
    result = cursor.fetchall()
    print(result)

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
    
    #create_table()
    #insert_userID('wayne')
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
    