import requests
import time
import configparser
from random_words import RandomWords
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import FirefoxOptions
from selenium import webdriver

def get_request(url, bearer_token):
    headers = {'Authorization': bearer_token}
    resp = requests.get(url, headers=headers)
    response = resp.json()
    return response

def post_request(url, data, bearer_token):
    headers = {'Authorization': bearer_token}
    resp = requests.post(url, data=data, headers=headers)
    return resp.json()

def parse_config():
    config = configparser.ConfigParser()
    config.read(".conf")
    user = config['account']['user']
    password = config['account']['password']
    encoding_token = "Bearer " + config['account']['encoding_token']
    decoding_token = "Bearer " + config['account']['decoding_token']
    type = config['account']['type']

    return user, password, encoding_token, decoding_token, type

def get_user_id(bearer_token):
    url = 'https://api.spotify.com/v1/me'
    response = get_request(url, bearer_token)
    return response['id']


def create_playlist(bearer_token):
    rw = RandomWords()
    user_id = get_user_id(bearer_token)
    url = 'https://api.spotify.com/v1/users/' + user_id + '/playlists'
    playlist_name = rw.random_word()
    data = '{"name":' + '"' + playlist_name + '", "description": "New Playlist", "public": true}'
    response = post_request(url, data, bearer_token)
    playlist_id = response['id']
    return playlist_id

def add_song_to_playlist(playlist_id, song, bearer_token):
    url = "https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks?uris=" + song
    post_request(url, "", bearer_token)

def selenium_interaction(user, password, playlist_name):
    opts= FirefoxOptions()
    opts.set_preference("media.eme.enabled",True)
    opts.set_preference("media.gmp-manager.updateEnabled",True)
    browser = webdriver.Firefox(options=opts)

    USERNAME_FIELD = (By.ID, "login-username")
    PASSWORD_FIELD = (By.ID, "login-password")
    NEXT_BUTTON = (By.ID, "login-button")
    WEB_PLAYER = (By.XPATH, "/html/body/div/div[2]/div/div/div[4]/div/a")
    PLAY_BUTTON = (By.XPATH, "/html/body/div[4]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[2]/div[2]/div/button[1]")

    try:
        if browser:
            browser.get("https://accounts.spotify.com/en/login")

        WebDriverWait(browser, 5).until(EC.element_to_be_clickable(USERNAME_FIELD)).send_keys(user)

        WebDriverWait(browser,5).until(EC.element_to_be_clickable(PASSWORD_FIELD)).send_keys(password)

        WebDriverWait(browser, 5).until(EC.element_to_be_clickable(NEXT_BUTTON)).click()

        WebDriverWait(browser, 5).until(EC.element_to_be_clickable(WEB_PLAYER)).click()

        browser.get("https://open.spotify.com/playlist/"+ playlist_name)
        time.sleep(5)
        
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable(PLAY_BUTTON)).click()

        time.sleep(1)

    except Exception as e:
        print(e)
        exit()


def start_playlist(user, password, type, playlist_name):

    if type == "free":
        print(playlist_name)
        selenium_interaction(user, password, playlist_name)
    else:
        pass
