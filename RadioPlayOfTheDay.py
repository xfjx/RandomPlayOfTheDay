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

# Die Playlisten kÃ¶nnen auch per Python angelegt werden, das darf aber nur 1x passieren!
#    results = spotify.user_playlist_create(user=username, name='TÃ¤glich neu: Benjamin BlÃ¼mchen', public=True) #, description='Jeden Tag ein anderes, zufÃ¤lligs HÃ¶rspiel von Benjamin BlÃ¼mchen')
#    results = spotify.user_playlist_create(user=username, name='TÃ¤glich neu: Bibi Blocksberg', public=True) #, description='Jeden Tag ein anderes, zufÃ¤lligs HÃ¶rspiel von Benjamin BlÃ¼mchen')
#    results = spotify.user_playlist_create(user=username, name='TÃ¤glich neu: Bibi und Tina', public=True) #, description='Jeden Tag ein anderes, zufÃ¤lligs HÃ¶rspiel von Benjamin BlÃ¼mchen')
#    results = spotify.user_playlist_create(user=username, name='TÃ¤glich neu: TKKG', public=True) #, description='Jeden Tag ein anderes, zufÃ¤lligs HÃ¶rspiel von Benjamin BlÃ¼mchen')
#    results = spotify.user_playlist_create(user=username, name='TÃ¤glich neu: Die drei ???', public=True) #, description='Jeden Tag ein anderes, zufÃ¤lligs HÃ¶rspiel von Benjamin BlÃ¼mchen')


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
            print "ungÃ¼ltiges Album!"
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
                print("Inhaltsangabe Ã¼bersprungen")

        print len(tracks), "Tracks..."
        while True:
            try:
                results = spotify.playlist_replace_items(playlist_id=artist['playlist'],items=playlist_tracks[0:99])

                # Da nicht mehr als 100 Tracks auf einmal hinzugefÃ¼gt werden dÃ¼rfen:
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
