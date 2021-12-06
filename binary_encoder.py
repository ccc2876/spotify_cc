from os import urandom
import random
from random_words import RandomWords 
from utils import *


def get_input():
    message = input("Enter the message to get: ")
    message = message.replace(" ", "")
    chars = list(message)
    return chars

def convert_to_binary(chars ):
    binary = ''.join(format(ord(char), '08b') for char in chars)
    return binary

def song_search(bearer_token):
    song = False
    while not song:
        rw = RandomWords()
        r = random.randint(0,100)
        search_term = rw.random_word()
        track_url = 'https://api.spotify.com/v1/search?q=' + search_term + '&type=track&limit=1&offset=' + str(r)
        response = get_request(track_url, bearer_token)
        if len(response['tracks']['items']) > 0:
            song = True
    return response

def parse_response(response):
    song_name = response['tracks']['items'][0]['name']
    explicit = response['tracks']['items'][0]['explicit']
    uri = response['tracks']['items'][0]['uri']

    return song_name, explicit, uri

def get_songs_for_playlist(binary, playlist_id, bearer_token):
    for num in binary:
        num = int(num)
        response = song_search(bearer_token)
        song_name, explicit, uri = parse_response(response)

        while (num==0 and explicit==True) or (num==1 and explicit==False):
            response = song_search(bearer_token)
            song_name, explicit, uri = parse_response(response)

        add_song_to_playlist(playlist_id, uri, bearer_token)
        print(str(num) + ": " + song_name + " with " + str(explicit) + " tag uploaded to playlist...")


def main():
    user, password, encoding_token, _ , type = parse_config()
    chars = get_input()
    binary = convert_to_binary(chars)
    playlist_id = create_playlist(encoding_token)
    get_songs_for_playlist(binary, playlist_id, encoding_token)
    print("Finished Uploading Playlist")
    start_playlist(user,password, type, playlist_id)
    


if __name__ == '__main__':
    main()