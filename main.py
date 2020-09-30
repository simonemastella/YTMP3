from pytube import YouTube
import os
from urllib import request
from urllib.request import urlopen
from html.parser import HTMLParser 

#pytube is a library under MIT license every right belongs to the author

def scrap(name):
    html = urlopen(name) 
    f=html.read().decode("utf-8")
    a=f.find(',"commandMetadata":{"webCommandMetadata":{"url":"/watch?v=')+58
    return f[a:a+11]



def download(url):
    #print(url)
    yt = YouTube(url)
    #video = yt.streams.first()     MP4
    video = yt.streams.filter(only_audio = True).first() # MP3
    out_file = video.download(output_path = "DOWNLOADS")
    base = os.path.splitext(out_file)
    new_file = base[0] + '.mp3'
    os.rename(out_file, new_file)
    print("LOG> video downloaded")

def oneSong(nome):
    base="https://www.youtube.com/"
    search="results?search_query="
    watch="watch?v="
    try:
        download(base+watch+scrap(base+search+nome.replace(" ","+")))
    except:
        print("ERROR CONTACT ME... www.mastella.eu")

if __name__== "__main__":
    print("TYPE exit TO QUIT THE PROGRAM")
    pick=input("TITLE:\t")
    while pick!="exit":
        oneSong(pick)
        pick=input("TITLE:\t")
