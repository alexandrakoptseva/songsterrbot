import requests
import xml.etree.ElementTree as ET


def artxml(artist_name: str, user_id: str):
    response = requests.get('http://www.songsterr.com/a/ra/songs/byartists.xml?artists="'+artist_name+'"')
    file_name = "./users_files/" + user_id + "-artist.xml"
    f1 = open(file_name, 'w')
    f1.write(response.text)


def songstr(song_id: str):
    response = requests.get('http://www.songsterr.com/a/wa/song?id='+ song_id)
    return response.url

