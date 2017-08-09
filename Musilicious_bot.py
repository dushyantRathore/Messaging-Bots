import telepot
from telepot.loop import MessageLoop
import time
import urllib
from pprint import pprint
import string
import requests
import json
from bs4 import BeautifulSoup
import codecs
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

    base_url = 'http://www.youtubeinmp3.com/fetch/?format=JSON&video='

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

    #print(l)
    youtube_url = "https://www.youtube.com" + l
    #print(youtube_url)
    download_url = base_url + str(youtube_url)
    print(download_url)

    # r = urllib.request.urlopen(download_url).read().decode('utf8')
    # data = json.loads(r)
    #
    # path = "/home/dushyant/Desktop/Github/Telegram-Bots/file.mp3"
    #
    # usock = urllib.request.urlopen(download_url)
    # print('info: ', usock.info())
    # f = open(path, 'wb')
    # try:
    #     file_size = int(usock.info().getheaders("Content-Length")[0])
    #     print('Downloading : %s Bytes: %s' % (path, file_size))
    # except IndexError:
    #     print('Unknown file size: index error')
    #
    # downloaded = 0
    # block_size = 8192
    # while True:
    #     buff = usock.read(block_size)
    #     if not buff:
    #         break
    #
    #     downloaded = downloaded + len(buff)
    #     f.write(buff)
    #     # download_status = r"%3.2f%%" % (downloaded * 100.00 / file_size)
    #     # download_status = download_status + (len(download_status)+1) * chr(8)
    #     # print download_status,"done"
    #
    # f.close()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == "text":
        message = msg["text"].lower()

        if message == '/start':
            bot.sendMessage(chat_id, "Please choose one of the following options : "
                                     "\n1. Get the lyrics of a song"
                                     "\n2. Download a song")

        elif message in ['hi', 'heyy', 'heya', 'hey', 'hello']:
            bot.sendMessage(chat_id, "Hi, please enter /start to use the features of the bot")

        elif message in ['1', '1.', '1)', '(1)']:
            bot.sendMessage(chat_id, "To get the lyrics of a song, provide the details in the following format : "
                                     "\n\nlyrics song 'Name of the song' by 'Name of the artist'")

        elif message in ['2', '2.', '2)', '(2)']:
            bot.sendMessage(chat_id, "To download a song, provide the details in the following format : "
                                     "\n\ndownload song 'Name of the song' by 'Name of the artist'")

        elif 'lyrics' in message:
            message = message.split()
            song_name_index = message.index("song")
            artist_name_index = message.index("by")

            song_name = "".join(message[song_name_index+1:artist_name_index])
            artist_name = "".join(message[artist_name_index+1:])

            #print(song_name)
            #print(artist_name)

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

            download_song(song_name, artist_name)


bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

# Keep the program running.
while 1:
    time.sleep(10)
