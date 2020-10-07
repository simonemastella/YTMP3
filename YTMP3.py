from pytube import YouTube
import os
from urllib import request
from urllib.parse import urlparse
from urllib.request import urlopen
from html.parser import HTMLParser 
from pyffmpeg import FFmpeg
import threading
#pytube is a library under MIT license every right belongs to the author

def scrap(name):
    try:
        html = urlopen(name) 
        f=html.read().decode("utf-8")
        a=f.find(',"commandMetadata":{"webCommandMetadata":{"url":"/watch?v=')+58
        return f[a:a+11]
    except:
        print("ERROR 421: scrap"+ name)

def download(url,nome):
    try:
        video = YouTube(url).streams.filter(only_audio = True).first() # MP3
        out_file = video.download()
        base = os.path.splitext(out_file)                
        convert(base[0])
        os.remove(base[0]+'.mp4')       
    except:
        print("ERROR 422: download"+ nome)
    
def convert(base):   
    ff=FFmpeg()
    ff.convert(base+'.mp4', base+'.mp3')


def oneSong(nome):
    base="https://www.youtube.com/"
    search=base+"results?search_query="
    watch=base+"watch?v="
    for c in nome:
        if ord(c)<128:
            search+=c
    download(watch+scrap(search.replace(" ","+")),nome)
    


if __name__== "__main__":
    print("""__   __________  _________ _____ 
\ \ / /_   _|  \/  || ___ \____ |
 \ V /  | | | .  . || |_/ /   / /
  \ /   | | | |\/| ||  __/    \ \\
  | |   | | | |  | || |   .___/ /
  \_/   \_/ \_|  |_/\_|   \____/
This Software is under MIT LICENSE
Developed by Simone Mastella
Visit www.mastella.eu
""")
    print("TYPE exit TO QUIT THE PROGRAM")
    pick=input("TITLE:\t")
    while pick!="exit":
        oneSong(pick)
        pick=input("TITLE:\t")
                      