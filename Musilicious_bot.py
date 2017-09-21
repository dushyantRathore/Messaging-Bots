import telepot
from bs4 import BeautifulSoup
import time
import urllib

TOKEN = '275551109:AAEC8iXZaCRKN2Kk_v6uYfa55QBQu5Hete0'


def get_lyrics(song,artist):

    url = "http://www.azlyrics.com/lyrics/" + artist + "/" + song + ".html"

    # add header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

    req = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener()
    response = opener.open(req)
    lyrics_html = response.read()

    soup = BeautifulSoup(lyrics_html, 'html.parser')

    # print(soup)

    l = []

    for div in soup.find_all('div', attrs={'class': 'col-xs-12 col-lg-8 text-center'}):
        for sub_div in div.find_all('div'):
            l.append(sub_div.text)

    l = map(lambda s: s.strip(), l)

    return l


def english_trending():

    url = "http://www.officialcharts.com/charts/mtv-urban-chart/"
    songs_file = urllib.request.urlopen(url)
    songs_html = songs_file.read()
    songs_file.close()

    soup = BeautifulSoup(songs_html, 'html.parser')

    song = []
    artist = []

    for d in soup.find_all("div", attrs={'class': 'title-artist'}):
        for s in d.find_all("div", attrs={'class' : 'title'}):
            song.append(s.text)

    for d in soup.find_all("div", attrs={'class': 'title-artist'}):
        for a in d.find_all("div", attrs={'class' : 'artist'}):
            artist.append(a.text)

    song = list(map(lambda s: s.strip(), song))
    artist = list(map(lambda s: s.strip(), artist))

    print(song)
    print(artist)

    return song,artist


def bollywood_trending():

    url = "https://www.saavn.com/s/featured/hindi/Weekly_Top_Songs"
    songs_file = urllib.request.urlopen(url)
    songs_html =songs_file.read()
    songs_file.close()

    soup = BeautifulSoup(songs_html,  "html.parser")

    song = []
    album = []

    for p in soup.find_all("p", attrs={"class": "song-name ellip"}):
        song.append(p.text)

    song = list(map(lambda s : s.strip(), song))

    for i in range(0, len(song)):
        song[i] = song[i].replace("\n", " - ")

    return song


def handle(msg):

    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == "text":
        message = msg["text"].lower()

        if message == '/start':

            bot.sendMessage(chat_id, "Please choose one of the following options : "
                                     "\n1. Get the lyrics of a song"
                                     "\n2. Get the trending english tracks"
                                     "\n3. Get the trending bollywood tracks")

        elif message in ['hi', 'heyy', 'heya', 'hey', 'hello']:

            bot.sendMessage(chat_id, "Hi, please enter /start to use the features of the bot")

        elif message in ['1', '1.', '1)', '(1)']:

            bot.sendMessage(chat_id, "To get the lyrics of a song, provide the details in the following format : "
                                     "\n\nlyrics song 'Name of the song' by 'Name of the artist'")

        elif message in ['2', '2.', '2)', '(2)']:

            bot.sendMessage(chat_id, "Getting the top english tracks for you.")

            song,artist = english_trending()

            result = ""

            for i in range(0,len(song)):
                result += "\n" + str(i+1) + ". " + str(song[i]) + "  -  " + str(artist[i]) + "\n"

            bot.sendMessage(chat_id, result)

        elif message in ['3', '3.', '3)', '(3)']:

            bot.sendMessage(chat_id, "Getting the trending bollywood tracks for you.")

            s = bollywood_trending()

            result = ""

            for i in range(0,len(s)):
                result += "\n" + str(i+1) + ". " + str(s[i]) + "\n"

            bot.sendMessage(chat_id, result)

        elif 'lyrics' in message:

            message = message.split()
            song_name_index = message.index("song")
            artist_name_index = message.index("by")

            song_name = "".join(message[song_name_index+1:artist_name_index])
            artist_name = "".join(message[artist_name_index+1:])

            l = get_lyrics(song_name,artist_name)
            l = list(l)
            lyrics = str(l[6])

            firstpart, secondpart = lyrics[:int(len(lyrics) / 2)], lyrics[int(len(lyrics) / 2):]

            bot.sendMessage(chat_id, firstpart)
            bot.sendMessage(chat_id, secondpart)


bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

# Keep the program running.
while 1:
    time.sleep(10)
