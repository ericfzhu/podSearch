import json
from pathlib import Path

import feedparser
import pandas as pd
import requests
import yt_dlp

import utils


def download_from_RSS(rss_url: str) -> None:
    """
    Download the RSS metadata from the podcast link
    :param rss_url:
    :return:
    """
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    # Create directory structure for feed if it doesn't already exist
    directory = utils.slugify(feed.feed.title)
    Path(f'data/{directory}').mkdir(parents=True, exist_ok=True)
    Path(f'data/{directory}/audio').mkdir(exist_ok=True)

    # Compare metadata with previous revision
    data = pd.DataFrame(feed.entries)
    if Path(f'data/{directory}/podcast.csv').exists():
        prev_data = pd.read_csv(f'data/{directory}/podcast.csv')
        entries = pd.concat([data, prev_data]).drop_duplicates(keep=False)
        entries['transcribed'] = False

        # Replace data with previous metadata to preserve transcribed column
        data = pd.concat([prev_data, entries], ignore_index=True)
    else:
        data['transcribed'] = False
        entries = data

    # Save metadata to JSON and CSV files
    data.to_csv(f'data/{directory}/metadata.csv', index=False)
    with open(f'data/{directory}/feed.json', 'w') as f:
        json.dump(feed.feed, f)

    # Download each podcast in the feed
    for i, entry in entries.iterrows():
        # Get the podcast URL
        podcast_url = next(link for link in entry.links if link.rel == 'enclosure').href

        # Download the podcast
        response = requests.get(podcast_url)

        # Save the podcast to a file
        file_name = utils.slugify(entry.title)
        with open(f'data/{directory}/audio/{file_name}.mp3', 'wb') as f:
            f.write(response.content)


def download_from_YT(channel_url: str):
    """
    Download the YT video from the link
    :param channel_url:
    :return:
    """
    ydl_opts = {
        'ignoreerrors': True,
        'abort_on_unavailable_fragments': True,
        'format': 'bestaudio/best',
        'outtmpl': 'YTChannels\%(uploader)s\%(title)s ## %(uploader)s ## %(id)s.%(ext)s',
        'ratelimit': 5000000,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(channel_url)
