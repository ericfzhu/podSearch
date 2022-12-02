import json
import feedparser
import pandas as pd
import requests
import validators
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

    # Save metadata to JSON and CSV files
    data = pd.DataFrame(feed.entries)
    data.to_csv('podcast.csv', index=False)
    with open('feed.json', 'w') as f:
        json.dump(feed.feed, f)

    # Download each podcast in the feed
    for entry in feed.entries:
        # Get the podcast URL
        podcast_url = entry.enclosures[0].href

        # Download the podcast
        response = requests.get(podcast_url)

        # Save the podcast to a file
        file_name = utils.slugify(entry.title)
        with open(file_name + '.mp3', 'wb') as f:
            f.write(response.content)


def download_from_YT(link: str):
    """
    Download the YT video from the link
    :param link:
    :return:
    """
    assert (validators.url(link))
