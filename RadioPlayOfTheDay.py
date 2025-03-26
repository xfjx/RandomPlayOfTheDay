#!/usr/bin/python2
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import sys
import spotipy
import spotipy.util as util
from pprint import pprint
from random import randint
import re
import os
import time
import json
os.chdir("/home/vossxebu/RadioPlayOfTheDay")

scope = 'user-library-read user-library-modify playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative user-follow-modify user-follow-read user-read-private user-read-email'
username = 'cn3capl0ebtv8nvgu2ahfvdsc'
token = util.prompt_for_user_token(username,scope,client_id='xxx',client_secret='xxx',redirect_uri='http://localhost:8080')

with open('RadioPlayOfTheDay.json', 'r') as json_data:
    artists = json.load(json_data)

if token:
    spotify = spotipy.Spotify(auth=token)

    album_types = ['single','album']

    for artist in artists:
        print artist['name']
        albums = []

        for album_type in album_types:
            print album_type
            while True:
                try:
                    results = spotify.artist_albums(artist['uri'], album_type=album_type)
                    albums.extend(results['items'])
                    while results['next']:
                        results = spotify.next(results)
                        albums.extend(results['items'])
                        print len(albums)
                except:
                    continue
                break

        random_album = randint(0,len(albums)-1)
#       print(albums[random_album]['name'])
        while not re.match(artist['match'],albums[random_album]['name']):
            print "ungültiges Album!"
            print albums[random_album]['name'];
            random_album = randint(0,len(albums)-1)

        print(albums[random_album]['name'])

        while True:
            try:
                results = spotify.album_tracks(albums[random_album]['uri'])
                tracks = results['items']
                while results['next']:
                    results = spotify.next(results)
                    tracks.extend(results['items'])
            except:
                continue
            break

        playlist_tracks = []
        for track in tracks:
            print(track['name'])
            if not re.match(".*Inhaltsangabe.*",track['name']):
                playlist_tracks.append(track['uri'])
            else:
                print("Inhaltsangabe übersprungen")

        print len(tracks), "Tracks..."
        while True:
            try:
                results = spotify.playlist_replace_items(playlist_id=artist['playlist'],items=playlist_tracks[0:99])

                # Da nicht mehr als 100 Tracks auf einmal hinzugefügt werden dürfen:
                x = 99
                while x < len(tracks):
                    results = spotify.playlist_add_items(playlist_id=artist['playlist'],items=playlist_tracks[x:x+99])
                    x+=99
            except:
                continue
            break
        time.sleep(5)

else:
    print "Can't get token for", username
