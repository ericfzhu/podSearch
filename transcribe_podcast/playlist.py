from youtubesearchpython import *
import pandas as pd
from yt_dlp import YoutubeDL


def get(channel_id):
    playlist = Playlist(playlist_from_channel_id(channel_id))

    print(f'Videos Retrieved: {len(playlist.videos)}')

    while playlist.hasMoreVideos:
        print('Getting more videos...')
        playlist.getNextVideos()
        print(f'Videos Retrieved: {len(playlist.videos)}')

    print('Found all the videos.')

    data = pd.DataFrame(playlist.videos)

    data.to_csv('playlist.csv', index=False)


def download():
    playlist = pd.read_csv('playlist.csv')

    for i, video in playlist.iterrows():
        with YoutubeDL({'paths': {"home": "/videos"}}) as ydl:
            ydl.download(video['link'])
