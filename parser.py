from bs4 import BeautifulSoup

name = "Back In Black"
soup = BeautifulSoup(open("artist.xml"), "html.parser")
songs = soup.find_all('song')
for song in songs:
    if song.title.contents[0] == name:
        print(song['id'])
        for t in song.find_all('tabtype'):
            print(t.next)
