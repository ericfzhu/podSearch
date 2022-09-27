import pandas as pd
from yt_dlp import YoutubeDL


playlist = pd.read_csv('playlist.csv')


for i, video in playlist.iterrows():
    with YoutubeDL({'paths': {"home": "/videos"}}) as ydl:
        ydl.download(video['link'])
