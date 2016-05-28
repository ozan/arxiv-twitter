#!/usr/bin/env python

from collections import namedtuple
from datetime import datetime
import logging
import os
import sys
import xml.etree.ElementTree as ET

import requests
import twitter

log = logging.getLogger()
log.addHandler(logging.StreamHandler(sys.stdout))

Article = namedtuple('Article', ('title', 'link', 'description'))
Tweet = namedtuple('Tweet', ('status',))
Source = namedtuple('Source', ('id', 'url'))

CONFIG = (
    # Computer Vision
    Source('CSCV', 'http://export.arxiv.org/rss/cs.CV'),
    # Computation and Language
    # Source('CSCL', 'http://export.arxiv.org/rss/cs.CL'),
    # Human Computer Interaction
    Source('CSHC', 'http://export.arxiv.org/rss/cs.HC'),
    # Graphics
    # Source('CSGR', 'http://export.arxiv.org/rss/cs.GR'),
)


def parse_articles(xml):
    """
    For the given string of arXiv.org RSS XML, return list of `Article`s
    """
    tree = ET.ElementTree(ET.fromstring(xml))
    ns = {'rss': 'http://purl.org/rss/1.0/'}
    items = tree.findall('rss:item', ns)
    return [
        Article(*[
            item.find('rss:{}'.format(field), ns).text
            for field in Article._fields
        ])
        for item in items
    ]


def tweet_for_article(article):
    """
    Construct a tweet for the given article
    """
    title = article.title.split('. (arXiv')[0]
    return Tweet('{} {}'.format(title, article.link))  # TODO < 140 chars


def send_tweet(api, tweet):
    """
    Actually POST tweet to twitter API
    """
    try:
        api.PostUpdate(tweet.status)
        log.info('Sent "{}"'.format(tweet.status))
    except twitter.TwitterError as e:
        log.warning('Failed to send "{}": {}'.format(tweet.status, e.message))


if __name__ == '__main__':
    log.info('Running run.py on {}'.format(datetime.now()))

    for source in CONFIG:
        res = requests.get(source.url)
        if not res.ok:
            log.warning('Failed on {}: {}'.format(source.url, res.reason))
            continue
        api = twitter.Api(
            consumer_key=os.environ['CONSUMER_KEY'],
            consumer_secret=os.environ['CONSUMER_SECRET'],
            access_token_key=os.environ[
                'ACCESS_TOKEN_KEY_{}'.format(source.id)],
            access_token_secret=os.environ[
                'ACCESS_TOKEN_SECRET_{}'.format(source.id)]
        )
        for article in parse_articles(res.text):
            send_tweet(api, tweet_for_article(article))
