Final Project:

Our app uses Spotify as OAuth to login and as its first API to determine the users' top playlist and favorite music genre. 
We then take this favorite music genre and go to our second API, Google Books. We find a book related to their favorite music genre
and generate it out. If the user chooses to, they can also decided to refresh the page and get another book suggestion. User information
is stored in the database. We remember the user id, playlist, favorite music genre and book title. When a user goes to our website we first check
to see if the user is already in our database or not. We ended up using Flask, Postgres and HTML/CSS.
