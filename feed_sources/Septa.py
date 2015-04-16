"""Fetch SEPTA (Philadelphia) bus and rail feeds."""

from datetime import datetime
import logging
import os
import zipfile

from bs4 import BeautifulSoup
import requests

from FeedSource import FeedSource

DEVELOPER_URL = 'http://www2.septa.org/developer/'
URL = DEVELOPER_URL + 'download.php'
LAST_UPDATED_FMT = '%a, %d %b %Y %H:%M:%S'

DOWNLOAD_FILE_NAME = 'septa.zip'
BUS_FILE = 'google_bus.zip'
RAIL_FILE = 'google_rail.zip'

LOG = logging.getLogger(__name__)


class Septa(FeedSource):
    """Fetch SEPTA feeds."""
    def __init__(self):
        super(Septa, self).__init__()
        self.urls = {DOWNLOAD_FILE_NAME: URL}

    def fetch(self):
        """Fetch SEPTA bus and rail feeds.

        First scrape the download page to see if a new feed is available,
        since the last-modified header is not set on the download.
        """
        get_septa = True
        page = requests.get(DEVELOPER_URL)
        LOG.debug('Checking last SEPTA update time...')
        last_mod = datetime.now().strftime(LAST_UPDATED_FMT)
        if page.ok:
            if page.ok:
                soup = BeautifulSoup(page.text)
                last_mod = soup.find('div', 'col_content').find('p').text
                LOG.info('SEPTA download last updated %s.', last_mod)
                last_mod = last_mod[14:] # trim out date string
                if self.timecheck.has_key(DOWNLOAD_FILE_NAME):
                    got_last = self.timecheck.get(DOWNLOAD_FILE_NAME)
                    if got_last == last_mod:
                        LOG.info('No new download available for SEPTA.')
                        get_septa = False
                    else:
                        LOG.info('New SEPTA download available.')
                        LOG.info('Latest SEPTA download posted: %s.', last_mod)
                        LOG.info('Previous download retrieved: %s.', got_last)
                else:
                    LOG.debug('No previous SEPTA download found.')
            else:
                LOG.debug('failed to get SEPTA dowload info page.')

            if get_septa:
                if self.download(DOWNLOAD_FILE_NAME, URL):
                    septa_file = os.path.join(self.ddir, DOWNLOAD_FILE_NAME)
                    if self.extract(septa_file):
                        self.timecheck[septa_file] = last_mod
                # delete download file once the two GTFS zips in it are extracted
                os.remove(septa_file)

    def extract(self, file_name):
        """Extract bus and rail GTFS files from downloaded zip, then validate each."""
        with zipfile.ZipFile(file_name) as zipped_septa:
            if len(zipped_septa.namelist()) == 2:
                zipped_septa.extractall(path=self.ddir)
                if os.path.isfile(BUS_FILE) and os.path.isfile(RAIL_FILE):
                    rail_good = bus_good = False
                    if self.verify(BUS_FILE):
                        self.new_use.append(BUS_FILE)
                        bus_good = True
                    else:
                        LOG.warn('SEPTA bus GTFS verification failed.')
                        return False
                    if self.verify(RAIL_FILE):
                        self.new_use.append(RAIL_FILE)
                        rail_good = True
                    else:
                        LOG.warn('SEPTA rail GTFS verification failed.')
                        return False
                    if rail_good and bus_good:
                        LOG.info('SEPTA bus and rail verification succeeded.')
                        return True
                else:
                    LOG.error('Could not find SEPTA GTFS files with expected names.')
                    return False
            else:
                LOG.error('Unexpected contents in SEPTA zip file download: %s',
                          zipped_septa.namelist())
                LOG.error('Expected two files, but got %s.',
                          len(zipped_septa.namelist()))
                LOG.error('Not extracting SEPTA zip.')
                return False

        LOG.error('How did we get here? In SEPTA extract.')
        return False # should be unreachable
