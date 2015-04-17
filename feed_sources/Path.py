"""Fetch PATH (NJ/NYC) feed."""

from datetime import datetime
import logging

from bs4 import BeautifulSoup
import requests

from FeedSource import FeedSource, TIMECHECK_FMT

URL = 'http://trilliumtransit.com/transit_feeds/path-nj-us/'
FILE_NAME = 'path.zip'
LAST_UPDATED_FMT = '%d-%b-%Y %H:%M'

LOG = logging.getLogger(__name__)


class Path(FeedSource):
    """Fetch PATH feed."""
    def __init__(self):
        super(Path, self).__init__()
        # The name of the download file changes on occasion.
        # Go scrape the directory listing to find out what it is now, and update url if found.
        self.urls = {FILE_NAME: URL + 'path-nj-us.zip'}
        response = requests.get(URL)
        if response.ok:
            soup = BeautifulSoup(response.text)
            anchors = soup.findAll('a')
            if len(anchors):
                # last link on the page shoud be our download
                lastlink = anchors[len(anchors)-1]
                # last updated time is in next column in table (last-modified header not set)
                last_updated_str = lastlink.findParent().findNextSibling().text.strip()
                self.last_updated = datetime.strptime(last_updated_str, LAST_UPDATED_FMT)
                filename = lastlink.text
                LOG.debug('Found PATH download file named %s, last updated: %s',
                          filename,
                          self.last_updated)
                download_url = URL + filename
                self.urls = {FILE_NAME: download_url}
            else:
                LOG.error('Could not parse directory listing for PATH.')
        else:
            LOG.error('Could not get directory listing for PATH.')

    def fetch(self):
        """No last-modified header set; check update time here."""
        if self.urls:
            stat = self.status.get(FILE_NAME)
            if stat:
                got_last = datetime.strptime(stat['posted_date'], TIMECHECK_FMT)
                if self.last_updated:
                    if got_last >= self.last_updated:
                        LOG.info('No new download found for PATH.')
                        self.update_existing_status(FILE_NAME)
                        return
                    else:
                        LOG.info('New download found for PATH posted: %s; last retrieved: %s',
                                 self.last_updated,
                                 got_last)
                else:
                    LOG.error('No last updated time found for PATH.')
                    self.last_updated = datetime.utcnow()
            else:
                LOG.info('No previous download found for PATH.')
                url = self.urls.get(FILE_NAME)

            # Download it and verify
            if self.fetchone(FILE_NAME, url):
                self.set_posted_date(FILE_NAME, self.last_updated.strftime(TIMECHECK_FMT))
                self.write_status()
        else:
            LOG.warn('No URLs to download for PATH.')
