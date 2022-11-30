from youtubesearchpython import *
import pandas as pd
from yt_dlp import YoutubeDL


def get(channel_id: str):
    playlist = Playlist(playlist_from_channel_id(channel_id))

    print(f'Videos Retrieved: {len(playlist.videos)}')

    while playlist.hasMoreVideos:
        print('Getting more videos...')
        playlist.getNextVideos()
        print(f'Videos Retrieved: {len(playlist.videos)}')

    print('Found all the videos.')

    return pd.DataFrame(playlist.videos)

    # data.to_csv('playlist.csv', index=False)


def download(playlist: pd.DataFrame):
    playlist = playlist['link'].tolist()

    ydl_opts = {
        'format': 'bestaudio/best',
        'paths': {"home": "/videos"}
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(playlist)
