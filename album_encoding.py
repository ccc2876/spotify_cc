import random
from utils import *

def get_input():
    message = input("Enter the message to get: ")
    message = message.replace(" ", "")
    chars = list(message)
    return chars

def get_songs_from_message(chars, playlist_id, bearer_token):
    for char in chars:
        album_name = ""
        while album_name=="" or album_name[0].upper()!=char.upper() or len(album_name)==1:
            r = random.randint(0,100)
            album_url = 'https://api.spotify.com/v1/search?q=' + char + '&type=album&limit=1&offset=' + str(r)
            response = get_request(album_url, bearer_token)
            album_name = response['albums']['items'][0]['name']
            album_id = response['albums']['items'][0]['id']
    
        album_songs_url = "https://api.spotify.com/v1/albums/" + album_id + "/tracks"
        response = get_request(album_songs_url, bearer_token)
        total_songs = response['total'] - 1
        r = random.randint(0, total_songs)

        song_url = "https://api.spotify.com/v1/albums/" + album_id + "/tracks?limit=1&offset=" + str(r)
        response = get_request(song_url, bearer_token)
        song_uri = response['items'][0]['uri']
        song_name = response['items'][0]['name']
        add_song_to_playlist(playlist_id, song_uri, bearer_token)
        print(char.upper() + ": " + song_name + " from the album " + album_name + " uploaded to playlist...")
    

def main():
    user, password, encoding_token, _ , type = parse_config()
    chars = get_input()
    playlist_id = create_playlist(encoding_token)
    get_songs_from_message(chars, playlist_id, encoding_token)
    print("Finished Uploading Playlist")
    start_playlist(user,password, type, playlist_id)
    


if __name__ == '__main__':
    main()