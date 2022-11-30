import validators
import requests
import xml.etree.ElementTree as ET
import feedparser
import pandas as pd
import json


def download_rss_metadata(link: str):
    """
    Download the RSS metadata from the podcast link
    :param link:
    :return:
    """
    response = requests.get(link)
    podcast = feedparser.parse(response.content)
    data = pd.DataFrame(podcast.entries)
    data['enclosure'] = [entry.enclosures[0].href for entry in podcast.entries]
    data.to_csv('podcast.csv', index=False)
    with open('feed.json', 'w') as f:
        json.dump(podcast.feed, f)


def download_YT(link: str):
    """
    Download the YT video from the link
    :param link:
    :return:
    """
    assert (validators.url(link))
