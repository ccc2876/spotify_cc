import json
import time
from Naked.toolshed.shell import muterun_js
from utils import *



def get_entry():
    naked_object = muterun_js("spotify-buddylist/example.js")
    friend_feed = naked_object.stdout.decode("utf-8")
    for entry in json.loads(friend_feed)['friends']:
        if entry['user']['name'] == 'undercover_agent':
            return entry
    return False


def get_playlist_info(playlist_uri, bearer_token):
    id = playlist_uri.split(":")[-1]
    url = "https://api.spotify.com/v1/playlists/" + id + "/tracks"
    response = get_request(url, bearer_token)
    message = ""
    explicit_song_list = []

    for item in response['items']:
        if item['track']['explicit'] is True:
            explicit_song_list.append('1')
        else:
            explicit_song_list.append('0')

        binary_string = ''.join(explicit_song_list)
        secret_message = ''.join(chr(int(binary_string[i * 8:i * 8 + 8], 2)) for i in range(len(binary_string) // 8))

    return secret_message

def main():
    user, password, _, decoding_token, type = parse_config()
    entry = get_entry()
    while not entry:
        entry = get_entry()
        print("Waiting for user to appear in friend feed...")

    playlist_uri = entry['track']['context']['uri']
    message = get_playlist_info(playlist_uri, decoding_token)
    print("Message is: ", message)



if __name__=='__main__':
    main()