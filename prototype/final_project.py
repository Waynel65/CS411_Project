#import flask
from flask import Flask, Response, request, session, render_template, redirect, url_for
import requests
import json
import time
#from flaskext.mysql import MySQL
#import flask_login

import base64
import os, base64

from PIL import Image
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth


#url_auth = 'https://accounts.spotify.com/authorize/?'
#url_token = 'https://accounts.spotify.com/api/token'

cid = 'f6e61fc841ba4eecad399452ae01c387'
secret = 'b74e2baa86894fcb8bf5db236d75597d'
scope = 'playlist-read-private'#playlist-read-collaborative user-top-read
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
		print("THE TOKEN IS INVALID")
		return
	
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

#TODO: still needs to work out the OAuth or else this function will keep getting json with error msg
def get_playlist():

	url = "https://api.spotify.com/v1/me/playlists"
	access_token = get_token()
	headers = {
		'Authorization': ('Bearer ' + access_token),
		'Content-Type': 'application/json'
	}

	try:
		response = requests.request("GET", url, headers=headers)
		jsonresp = response.json()
		# print(jsonresp)
	except:
		print("OAuth Token has Expired")
		return render_template('song.html', message= 'OAuth Token has expired')

	return jsonresp ## this is temporary for testing purposes



	


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