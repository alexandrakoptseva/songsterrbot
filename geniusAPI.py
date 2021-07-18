import os
import lyricsgenius
from dotenv import load_dotenv

config = load_dotenv()
token = os.getenv("geniusapikey")

genius = lyricsgenius.Genius(token)


def get_lyrics(artist: str, songname: str):
    artist = genius.search_artist(artist, max_songs=1, sort="title")
    song = artist.song(songname)
    return str(song.lyrics)


def get_artist_description(artist: str):
    artist = genius.search_artist(artist, max_songs=1, sort="title")
    return str(artist._body['description']['plain'])
