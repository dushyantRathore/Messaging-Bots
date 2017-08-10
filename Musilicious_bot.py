import telepot
import json
from bs4 import BeautifulSoup
import time
import urllib
import os
import urllib3
import youtube_dl

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

    #  print(soup)

    l = []

    for div in soup.find_all('div', attrs={'class': 'col-xs-12 col-lg-8 text-center'}):
        for sub_div in div.find_all('div'):
            l.append(sub_div.text)

    l = map(lambda s: s.strip(), l)

    return l


def download_song(song, artist):

    base_url = 'http://www.youtubeinmp3.com/fetch/?format=JSON&video='  # Youtube MP3 url

    x = song + "by" + artist

    query = x.lower()
    quoted_query = urllib.parse.quote(query)

    url = "https://www.youtube.com/results?search_query=" + quoted_query

    # add header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

    req = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener()
    response = opener.open(req)
    data_html = response.read()
    opener.close()

    soup = BeautifulSoup(data_html, 'html.parser')

    # print(soup)

    ref = []
    x = []

    for h3 in soup.find("h3", attrs={"class": "yt-lockup-title"}):
        x.append(h3)

    del(x[1])

    s = str(x[0])

    l = s.split("href=")
    del(l[0])
    l = str(l[0])
    l = l.split(" ")
    l = str(l[0])

    l = l.replace('"', '')

    # print(l)

    youtube_url = "https://www.youtube.com" + l
    print("Youtube URL : " + str(youtube_url))

    download_url = base_url + str(youtube_url)
    # print(download_url)

    r = urllib.request.urlopen(download_url).read().decode('utf8')
    data = json.loads(r)

    title = data['title']
    length = data['length']

    file_name = str(title) + ".mp3" # File name for the downloaded file

    if not os.path.exists(file_name):

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': file_name
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

    else:
        print("File already exists")

    return file_name,length


def billboard_trending():

    url = "http://www.billboard.com/charts/hot-100"
    songs_file = urllib.request.urlopen(url)
    songs_html = songs_file.read()
    songs_file.close()

    soup = BeautifulSoup(songs_html, 'html.parser')

    title = soup.find_all('div', attrs={'class': 'chart-row__title'})

    song = []
    artist = []

    for i in title:
        head = i.find("h2")
        song.append(head.text)

    for a in soup.find_all("a", attrs={'class': 'chart-row__artist'}):
        artist.append(a.text)

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
                                     "\n2. Download a song"
                                     "\n3. Get the top tracks on billboard"
                                     "\n4. Get the trending bollywood tracks")

        elif message in ['hi', 'heyy', 'heya', 'hey', 'hello']:

            bot.sendMessage(chat_id, "Hi, please enter /start to use the features of the bot")

        elif message in ['1', '1.', '1)', '(1)']:

            bot.sendMessage(chat_id, "To get the lyrics of a song, provide the details in the following format : "
                                     "\n\nlyrics song 'Name of the song' by 'Name of the artist'")

        elif message in ['2', '2.', '2)', '(2)']:

            bot.sendMessage(chat_id, "To download a song, provide the details in the following format : "
                                     "\n\ndownload song 'Name of the song' by 'Name of the artist'")

        elif message in ['3', '3.', '3)', '(3)']:

            bot.sendMessage(chat_id, "Getting the top tracks on billboard for you.")

            song,artist = billboard_trending()

            result = ""

            for i in range(0,10):
                result += "\n" + str(i+1) + ". " + str(song[i]) + "  -  " + str(artist[i])

            bot.sendMessage(chat_id, result)

        elif message in ['4', '4.', '4)', '(4)']:

            bot.sendMessage(chat_id, "Getting the trending bollywood tracks for you.")

            s = bollywood_trending()

            result = ""

            for i in range(0,10):
                result += "\n" + str(i+1) + ". " + str(s[i])

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

        elif 'download' in message:

            message = message.split()
            song_name_index = message.index("song")
            artist_name_index = message.index("by")

            song_name = "".join(message[song_name_index + 1:artist_name_index])
            artist_name = "".join(message[artist_name_index + 1:])

            bot.sendMessage(chat_id, "Relax, I'm getting your song..")

            file,length = download_song(song_name, artist_name)

            audio = open(file, 'rb')
            bot.sendAudio(chat_id, audio)

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))


bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

# Keep the program running.
while 1:
    time.sleep(10)
