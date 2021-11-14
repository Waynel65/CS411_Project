import flask
from flask import Flask, Response, request, render_template, redirect, url_for
import requests
import json
#from flaskext.mysql import MySQL
#import flask_login

import os, base64
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from PIL import Image
from io import BytesIO



cid = 'f6e61fc841ba4eecad399452ae01c387'
secret = 'b74e2baa86894fcb8bf5db236d75597d'

#client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
#spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

app = Flask(__name__)

#print(spotify.current_user())


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


@app.route("/", methods=['GET'])
def hello():
	return render_template('hello.html', message= 'Welcome')


@app.route("/songsearch", methods=['GET'])
def song():
	return render_template('song.html')

@app.route("/songsearch/", methods=['POST'])
def displaysearch():
	try:
		song = request.form.get('song_title')
	except:
		print("couldn't find all tokens")
		return render_template('song.html', message='error')
    #TODO: send query to api and recieve json for book and extract author from json
	song = song.replace(" ","%20")

	url = "https://api.spotify.com/v1/search?q=" + song + "&type=track&limit=1"

	payload={}
	OAuthToken = 'BQCqORPKzmlkfP_3iAgzh-VlsFFSghvVskZyFXhufRIdmh19G2f6KvJLRE7ymx8BPQHZMK9LFzrWiML3J9IcSeu11ZF0L5hnBrcWRBpBWIj9V4yMz3Lx-awUlIRAr06eu-EOnV7hpVk2tR-xhAE0q_G0A3tgdwObP_k'
	info = "Below is the artist of the song:"
	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Authorization': ('Bearer ' + OAuthToken)
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


if __name__ == "__main__":
	app.run(debug=True)