import json
import feedparser
import pandas as pd
import requests
import validators
import utils
import os


def download_from_RSS(rss_url: str) -> None:
    """
    Download the RSS metadata from the podcast link
    :param rss_url:
    :return:
    """
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    # Create directory for feed if it doesn't already exist
    directory = utils.slugify(feed.feed.title)
    os.makedirs(directory, exist_ok=True)
    os.makedirs(f'{directory}/audio', exist_ok=True)

    # Compare metadata with previous revision
    data = pd.DataFrame(feed.entries)
    if os.path.exists(f'{directory}/podcast.csv'):
        prev_data = pd.read_csv(f'{directory}/podcast.csv')
        entries = pd.concat([data, prev_data]).drop_duplicates(keep=False)
    else:
        entries = data

    # Save metadata to JSON and CSV files
    data.to_csv(f'{directory}/podcast.csv', index=False)
    with open(f'{directory}/feed.json', 'w') as f:
        json.dump(feed.feed, f)

    # Download each podcast in the feed
    for entry in entries:
        # Get the podcast URL
        podcast_url = next(x for x in entry['links'] if x['rel'] == 'enclosure').href

        # Download the podcast
        response = requests.get(podcast_url)

        # Save the podcast to a file
        file_name = utils.slugify(entry.title)
        with open(f'{directory}/audio/{file_name}.mp3', 'wb') as f:
            f.write(response.content)


def download_from_YT(link: str):
    """
    Download the YT video from the link
    :param link:
    :return:
    """
    assert (validators.url(link))
