"""Fetch Port Authority of Allegheny County (Pittsburgh) feed."""
from datetime import datetime
import logging

from bs4 import BeautifulSoup
import requests

from FeedSource import FeedSource, TIMECHECK_FMT

URL = 'http://www.portauthority.org/GeneralTransitFeed/'
FILE_NAME = 'paac.zip'

LOG = logging.getLogger(__name__)


class Paac(FeedSource):
    """Fetch Pittsburgh feed."""
    def __init__(self):
        super(Paac, self).__init__()
        # Go scrape the directory listing to find out what download file name is
        response = requests.get(URL)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            # go find the zip file link
            anchors = soup.findAll('a')
            for anchor in anchors:
                if anchor.text.endswith('.zip'):
                    LOG.debug('Found PAAC download file named %s', anchor.text)
                    self.urls = {FILE_NAME: URL + anchor.text}
            if not self.urls:
                LOG.error('Could not parse directory listing for PAAC.')
        else:
            LOG.error('Could not get directory listing for PAAC.')
