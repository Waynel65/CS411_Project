#import flask
from flask import Flask, Response, request, session, render_template, redirect, url_for
import requests
import json
import time
from random import randrange

import base64
import os, base64
from collections import Counter

from PIL import Image
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from postgres import *


#url_auth = 'https://accounts.spotify.com/authorize/?'
#url_token = 'https://accounts.spotify.com/api/token'

cid = 'f6e61fc841ba4eecad399452ae01c387'
secret = 'b74e2baa86894fcb8bf5db236d75597d'
scope = 'playlist-read-private'
# scope = 'user-library-read'
redirect_uri = 'http://127.0.0.1:5000/authorize'

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'


# app.secret_key = 'super secret string'  # Change this!

# #These will need to be changed according to your creditionals
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = '8976'
# app.config['MYSQL_DATABASE_DB'] = 'photoshare'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

# @app.route('/some-url')
# def get_data():
#     return requests.get('http://example.com').content


def create_spotify_oauth():
	return SpotifyOAuth(client_id = cid, client_secret = secret, redirect_uri= url_for('authorize', _external=True), scope = scope)

def get_token():
    token_valid = False
    token_info = session.get("token_info", {})
    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid

# @app.route("/", methods=['GET'])
# def hello():
# 	return render_template('hello.html', message= 'Welcome')

@app.route("/")
def login():

	## connecting to database

	conn, cursor = get_db_connection()
	create_table(conn, cursor)
	conn.close()

	## Oauth
	sp_oauth = create_spotify_oauth()
	auth_url = sp_oauth.get_authorize_url()
	print(auth_url)
	return redirect(auth_url)

@app.route("/authorize")
def authorize():
	sp_oauth = create_spotify_oauth()
	session.clear()
	code = request.args.get('code')
	token_info = sp_oauth.get_access_token(code) ## token info contains access token and refresh token
	session["token_info"] = token_info
	# return "redirect successfully"
	return redirect(url_for('song', _external=True))



@app.route("/song", methods=['GET'])
def song(): ## app route must match function name otherwise wont work
	session['token_info'], authorized = get_token()

	#session.modified = True
	if not authorized:
		return render_template('unauthorized.html')
	else:
		sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))

		## storing user name in database
		store_user_data()
		
		return render_template('hello.html', message="Welcome!")


@app.route("/songsearch", methods=['GET'])
def songsearch():
	return render_template('song.html')

@app.route("/displaysearch", methods=['POST'])
def displaysearch():
	try:
		song = request.form.get('song_title') ## get input from webpage
	except:
		print("couldn't find all tokens")
		return render_template('song.html', message='error')
    #TODO: send query to api and recieve json for book and extract author from json
	song = song.replace(" ","%20")
	url = "https://api.spotify.com/v1/search?q=" + song + "&type=track&limit=1"

	payload={}
	token_info, token_valid = get_token()
	if(not token_valid):
		return render_template('song.html', message='TOKEN INVALID')
	
	accessToken = token_info['access_token']

	info = "Below is the artist of the song:"
	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Authorization': ('Bearer ' + accessToken)
	}
	#the authorization changes based on the OAuth token temporary

	try:
		response = requests.request("GET", url, headers=headers, data=payload)
		jsonresp = response.json()
		artistname = jsonresp['tracks']['items'][0]['album']['artists'][0]['name']
		artistpic = jsonresp['tracks']['items'][0]['album']['images'][0]['url']
		artistlink = jsonresp['tracks']['items'][0]['album']['artists'][0]['external_urls']['spotify']
		return render_template('song.html', info=info, artist=artistname, album=artistpic, link=artistlink)
	except:
		print("OAuth Token has Expired")
		return render_template('song.html', message= 'OAuth Token has expired')

@app.route("/displaybook", methods = ['GET','POST'])
def displaybook():
	#TODO: use database to calculate the most popular genre in the playlist
	conn, cursor = get_db_connection()
	genre = get_user_music_genre(conn, cursor,get_current_user_name())
	print(type(genre))
	print(genre)
	key = "&key=AIzaSyCUbOUuw8As3ge_lxljneppox9WbTHimrU"
	q = "q=subject:" + genre.replace(" ", "_")
	url = "https://www.googleapis.com/books/v1/volumes?" + q + key
	print(url)
	try:
		response = requests.request("GET", url)
		jsonresp = response.json()
		#print(jsonresp)
		size = len(jsonresp['items'])
		print("size: " + str(size))
		randint = randrange(size)
		random_book = jsonresp['items'][randint]['volumeInfo']['title']
		print(random_book)
		thumbnail = jsonresp['items'][randint]['volumeInfo']['imageLinks']['thumbnail']
		link = jsonresp['items'][randint]['volumeInfo']['canonicalVolumeLink']
		print(thumbnail)
		print("------------" + random_book + "------------------")
		return render_template("book.html", genre=genre, bookname=random_book, picture = thumbnail, link=link)
	except:
		print("ERROR GET BOOK")
		return render_template('book.html', message= "testing error")


def get_current_user_name():
	token_info, token_valid = get_token()
	if(not token_valid):
		return render_template('song.html', message='TOKEN INVALID')
	
	access_token = token_info['access_token']
	sp = spotipy.Spotify(auth=access_token)

	user_name = sp.current_user()
	try:
		return user_name['display_name']
	except:
		return render_template('song.html', message='user_name error')

# @app.route("/get_playlist")
def get_playlist():
	'''
		returns the ID (in string) of the very first playlist of user's library
	'''

	# url = "https://api.spotify.com/v1/me/playlists"
	token_info, token_valid = get_token()
	if(not token_valid):
		return render_template('song.html', message='TOKEN INVALID')
	
	access_token = token_info['access_token']
	sp = spotipy.Spotify(auth=access_token)

	playlists = sp.current_user_playlists(limit=10)
	# print(type(playlists))
	# print(playlists)
	try:
		first_playlist_id = playlists['items'][0]['id']
		return str(first_playlist_id)
	except:
		return render_template('song.html', message='Playlist not found')
	# print(first_playlist_id)
	
# @app.route("/getItems")
def get_playlist_items(id):
	'''
		return a list of songs from the given playlist id
	'''
	# id = '7jG9s2hN1UD1dUKGfeA1ED'
	token_info, token_valid = get_token()
	if(not token_valid):
		return render_template('song.html', message='TOKEN INVALID')
	
	access_token = token_info['access_token']
	sp = spotipy.Spotify(auth=access_token)

	song_list = sp.playlist_items(id, limit=100)

	try:
		item_list = song_list['items']
		# print(item_list)
		return item_list
	except:
		print('error')
		return render_template('song.html', message='items not found')

# @app.route("/getGenre")
def get_artist_genre(artist_id):
	# artist_id = "07ZhipyrvoyNoJejeyM0PQ"
	token_info, token_valid = get_token()
	if(not token_valid):
		return render_template('song.html', message='TOKEN INVALID')
	
	access_token = token_info['access_token']
	sp = spotipy.Spotify(auth=access_token)

	artist = sp.artist(artist_id)
	try:
		artist_genre_list = artist['genres']
		# print(item_list)
		return artist_genre_list
	except:
		print('error')
		return render_template('song.html', message='items not found')

	return

# @app.route("/get_genre_list")
def get_genre_list(playlist_id):
	song_list = get_playlist_items(playlist_id)

	genre_list = []
	for i in range(len(song_list)):
		artist_id = song_list[i]['track']['artists'][0]['id']
		genres = get_artist_genre(artist_id)
		for artist_genre in genres:
			genre_list.append(artist_genre)
	
	return genre_list
#TODO: read genre list from database
@app.route("/get_genre_list")
def get_top_genre(genre_list):
	# genre_list = get_genre_list()
	return max(genre_list, key=genre_list.count)

def store_user_data():
    
	## store userID in DB

	conn, cursor = get_db_connection()
	username = get_current_user_name()
	insert_userID(conn, cursor, username)
	## get and store playlist

	playlist_id = get_playlist()
	# print(play_list_id)
	insert_playlist(conn, cursor, username, playlist_id)
	genre_list = get_genre_list(playlist_id) ## impacts performance quite a bit

	top_genre = get_top_genre(genre_list)
	insert_music_genre(conn, cursor, username, top_genre)

	## still need to read from DB the genre list
	conn.close()

	return

#TODO: still need to design a version where everything directly retrives from DB

# Documentation on how to request a new token is here:
# https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/

# def get_token():
#   tokenUrl = "https://accounts.spotify.com/api/token"
#   # The client ID and secret must be encoded as a base 64 string
#   binary = base64.b64encode(bytes(cid + ":" + secret, "utf-8"))
#   authToken = binary.decode("ascii")
#   headers = {
#     "Authorization": "Basic " + authToken
#   }
#   payload = {
#     "grant_type": "client_credentials"
#   }
#   response = requests.request("POST", tokenUrl, headers=headers, data=payload)
#   json = response.json()
#   return json["access_token"]


if __name__ == "__main__":
	app.run(debug=True)