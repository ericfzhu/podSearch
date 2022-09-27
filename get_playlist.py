from youtubesearchpython import *
import pandas as pd

channel_id = "UCESLZhusAkFfsNsApnjF_Cg"
playlist = Playlist(playlist_from_channel_id(channel_id))

print(f'Videos Retrieved: {len(playlist.videos)}')

while playlist.hasMoreVideos:
    print('Getting more videos...')
    playlist.getNextVideos()
    print(f'Videos Retrieved: {len(playlist.videos)}')

print('Found all the videos.')

data = pd.DataFrame(playlist.videos)

data.to_csv('playlist.csv', index=False)
