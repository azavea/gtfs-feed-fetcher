"""Fetch PATH (NJ/NYC) feed."""
import logging

from bs4 import BeautifulSoup
import requests

from FeedSource import FeedSource

URL = 'http://trilliumtransit.com/transit_feeds/path-nj-us/'

LOG = logging.getLogger(__name__)


class Path(FeedSource):
    """Fetch PATH feed."""
    def __init__(self):
        super(Path, self).__init__()
        self.urls = {'path.zip': URL + 'path-nj-us.zip'}
        # The name of the download file changes on occasion.
        # Go scrape the directory listing to find out what it is now, and update url if found.
        response = requests.get(URL)
        if response.ok:
            soup = BeautifulSoup(response.text)
            anchors = soup.findAll('a')
            if len(anchors):
                # last link on the page shoud be our download
                lastlink = anchors[len(anchors)-1]
                filename = lastlink.text
                LOG.debug('Found PATH download file name of %s.', filename)
                download_url = URL + filename
                self.urls = {'path.zip': download_url}
            else:
                LOG.error('Could not parse directory listing for PATH.')
        else:
            LOG.error('Could not get directory listing for PATH.')
