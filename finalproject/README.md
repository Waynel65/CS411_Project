Make sure to install all imports:
    pip install flask
    pip install requests
    pip install pillow

To run, just type "py 411Project" in terminal
The website should be displayed in address http://127.0.0.1:5000/

You need to change the value of OAuthToken in the python code to a valid token
link to OAuth Token Generator: https://developer.spotify.com/console/get-search-item/ 


Final Project Description:

Our app uses Spotify as OAuth to login and as its first API to determine the users' top playlist and favorite music genre. We then take this favorite music genre and go to our second API, Google Books. We find a book related to their favorite music genre and generate it out. If the user chooses to, they can also decided to refresh the page and get another book suggestion. User information is stored in the database. We remember the user id, playlist, favorite music genre and book title. When a user goes to our website we first check to see if the user is already in our database or not. We ended up using Flask, Postgres and HTML/CSS.
