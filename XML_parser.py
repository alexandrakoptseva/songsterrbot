import requests
from bs4 import BeautifulSoup


def xml_songs_parser(user_id: str):
    tab_list = []
    file_name = "./users_files/" + user_id + "-artist.xml"
    output_file = "./users_files/" + user_id + "-songs.txt"
    soup = BeautifulSoup(open(file_name), "html.parser")
    songs = soup.find_all('song')
    i = 0
    f1 = open(output_file, 'w')
    for song in songs:
        i += 1
        f1.write(str(i))
        f1.write(" - ")
        f1.write(song.title.contents[0])
        f1.write("  | song id = ")
        f1.write(str(song['id']))
        f1.write("\n")


def xml_songid_parser(name: str, user_id: str):
    tab_list = []
    file_name = "./users_files/" + user_id + "-artist.xml"
    soup = BeautifulSoup(open(file_name), "html.parser")
    songs = soup.find_all('song')
    for song in songs:
        if song.title.contents[0] == name:
            song_id = song['id']
    return song_id
