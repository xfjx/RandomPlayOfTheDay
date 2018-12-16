#!/usr/local/bin/python2
# -*- coding: utf-8 -*-

import sys
import spotipy
import spotipy.util as util
import numpy
from pprint import pprint
from random import randint
import re

scope = 'user-library-read user-library-modify playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative user-follow-modify user-follow-read user-read-private user-read-email'
username = '*****'
token = util.prompt_for_user_token(username,scope,client_id='*****',client_secret='*****',redirect_uri='http://localhost')

artists = []

# Bibi Blocksberg
artist = {"name" : "Bibi Blocksberg", "uri":"spotify:artist:3t2iKODSDyzoDJw7AsD99u", "playlist":"spotify:user:cn3capl0ebtv8nvgu2ahfvdsc:playlist:3VImPHL1gckY0axplKMhal", "match": "Folge", "album_type":"album"}
artists.append(artist)

# Bibi und Tina
artist = {"name" : "Bibi und Tina", "uri":"spotify:artist:2x8vG4f0HYXzMEo3xNsoiI", "playlist":"spotify:user:cn3capl0ebtv8nvgu2ahfvdsc:playlist:2hUN7xBubyoW0kPBZyYtKH", "match":"Folge", "album_type":"album"}
artists.append(artist)

# Benjamin Blümchen
artist = {"name" : "Benjamin Blümchen", "uri":"spotify:artist:1l6d0RIxTL3JytlLGvWzYe", "playlist":"spotify:user:cn3capl0ebtv8nvgu2ahfvdsc:playlist:3w5mJesfrZrGN3jSjPJG1t", "match":"Folge", "album_type":"album"}
artists.append(artist)

# Die drei ???
artist = {"name" : "Die drei ???", "uri":"spotify:artist:3meJIgRw7YleJrmbpbJK6S", "playlist":"spotify:user:cn3capl0ebtv8nvgu2ahfvdsc:playlist:0QRh6dDWyOtS4AX1xyFkDy", "match":"", "album_type":"album"}
artists.append(artist)

# TKKG
artist = {"name" : "TKKG", "uri":"spotify:artist:61qDotnjM0jnY5lkfOP7ve", "playlist":"spotify:user:cn3capl0ebtv8nvgu2ahfvdsc:playlist:57MRp4abeiVLfS8tBE9n6q", "match":"", "album_type":"album"}
artists.append(artist)

# TKKG Retro
artist = {"name" : "TKKG-Retro", "uri":"spotify:artist:0i38tQX5j4gZ0KS3eCMoIl", "playlist":"spotify:user:cn3capl0ebtv8nvgu2ahfvdsc:playlist:4ePpHGeJKtDI6NMJ3vEg2P","match":"", "album_type":"single"}
artists.append(artist)

if token:
    spotify = spotipy.Spotify(auth=token)

# Die Playlisten können auch per Python angelegt werden, das darf aber nur 1x passieren!
#    results = spotify.user_playlist_create(user=username, name='Täglich neu: Benjamin Blümchen', public=True) #, description='Jeden Tag ein anderes, zufälligs Hörspiel von Benjamin Blümchen')
#    results = spotify.user_playlist_create(user=username, name='Täglich neu: Bibi Blocksberg', public=True) #, description='Jeden Tag ein anderes, zufälligs Hörspiel von Benjamin Blümchen')
#    results = spotify.user_playlist_create(user=username, name='Täglich neu: Bibi und Tina', public=True) #, description='Jeden Tag ein anderes, zufälligs Hörspiel von Benjamin Blümchen')
#    results = spotify.user_playlist_create(user=username, name='Täglich neu: TKKG', public=True) #, description='Jeden Tag ein anderes, zufälligs Hörspiel von Benjamin Blümchen')
#    results = spotify.user_playlist_create(user=username, name='Täglich neu: Die drei ???', public=True) #, description='Jeden Tag ein anderes, zufälligs Hörspiel von Benjamin Blümchen')

    for artist in artists:
	print artist['name']
	results = spotify.artist_albums(artist['uri'], album_type=artist['album_type'])
	albums = results['items']
	while results['next']:
	    results = spotify.next(results)
	    albums.extend(results['items'])

	random_album = randint(0,len(albums)-1)
	print(albums[random_album]['name'])
	while not re.match(artist['match'],albums[random_album]['name']):
	    print "ungültiges Album!"
    	    random_album = randint(0,len(albums)-1)
	    print(albums[random_album]['name'])

	results = spotify.album_tracks(albums[random_album]['uri'])
	tracks = results['items']
	while results['next']:
	    results = spotify.next(results)
	    tracks.extend(results['items'])

	playlist_tracks = []
	for track in tracks:
	    playlist_tracks.append(track['uri'])

	print len(tracks), "Tracks..."
	results = spotify.user_playlist_replace_tracks(user=username,playlist_id=artist['playlist'],tracks=playlist_tracks[0:99])

	# Da nicht mehr als 100 Tracks auf einmal hinzugefügt werden dürfen:
	x = 99
	while x < len(tracks):
	    results = spotify.user_playlist_add_tracks(user=username,playlist_id=artist['playlist'],tracks=playlist_tracks[x:x+99])
	    x+=99

else:
    print "Can't get token for", username
