import requests
import json
from random import randrange

def get_rand_book(bname):
    key = "&key=AIzaSyCUbOUuw8As3ge_lxljneppox9WbTHimrU"
    q = "q=subject:" + bname.replace(" ", "_")
    url = "https://www.googleapis.com/books/v1/volumes?" + q + key
    print(url)
    try:
        response = requests.request("GET", url)
        jsonresp = response.json()
        size = len(jsonresp['items'])
        print(jsonresp['items'][randrange(size)]['volumeInfo']['title'])
    except:
        print("ERROR GET BOOK")

def main():
    get_rand_book("Rap")

if __name__ == "__main__":
    main()
    