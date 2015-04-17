"""Fetch SEPTA (Philadelphia) bus and rail feeds."""

from datetime import datetime
import logging
import os
import zipfile

from bs4 import BeautifulSoup
import requests

from FeedSource import FeedSource, TIMECHECK_FMT

DEVELOPER_URL = 'http://www2.septa.org/developer/'
URL = DEVELOPER_URL + 'download.php'
LAST_UPDATED_FMT = '%a, %d %b %Y %H:%M:%S'

# SEPTA provides two GTFS .zip files themselves zipped together
DOWNLOAD_FILE_NAME = 'septa.zip'
# names of the two files in the downloaded .zip
BUS_EXTRACT_FILE = 'google_bus.zip'
RAIL_EXTRACT_FILE = 'google_rail.zip'
# rename the extrated GTFS to this
BUS_FILE = 'septa_bus.zip'
RAIL_FILE = 'septa_rail.zip'

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
        page = requests.get(DEVELOPER_URL)
        LOG.debug('Checking last SEPTA update time...')
        last_mod = datetime.utcnow()
        if page.ok:
            soup = BeautifulSoup(page.text)
            last_mod = soup.find('div', 'col_content').find('p').text
            LOG.info('SEPTA download page: %s.', last_mod)
            last_mod_str = last_mod[14:]  # trim out date string
            last_mod = datetime.strptime(last_mod_str, LAST_UPDATED_FMT)  # convert to date
            stat = self.status.get(BUS_FILE)
            posted_date = last_mod.strftime(TIMECHECK_FMT)
            if stat:
                got_last = datetime.strptime(stat['posted_date'], TIMECHECK_FMT)
                if got_last >= last_mod:
                    LOG.info('No new download available for SEPTA.')
                    self.update_existing_status(BUS_FILE)
                    self.update_existing_status(RAIL_FILE)
                    return
                else:
                    LOG.info('New SEPTA download available.')
                    LOG.info('Latest SEPTA download posted: %s.', last_mod)
                    LOG.info('Previous download retrieved: %s.', got_last)
                    self.set_posted_date(BUS_FILE, posted_date)
                    self.set_posted_date(RAIL_FILE, posted_date)
            else:
                LOG.debug('No previous SEPTA download found.')
        else:
            LOG.error('failed to get SEPTA dowload info page.')

        if self.download(DOWNLOAD_FILE_NAME, URL):
            septa_file = os.path.join(self.ddir, DOWNLOAD_FILE_NAME)
            if self.extract(septa_file):
                self.write_status()
            # delete download file once the two GTFS zips in it are extracted
            os.remove(septa_file)

    def extract(self, file_name):
        """Extract bus and rail GTFS files from downloaded zip, then validate each."""
        with zipfile.ZipFile(file_name) as zipped_septa:
            if len(zipped_septa.namelist()) == 2:
                zipped_septa.extractall(path=self.ddir)
                bus_path = os.path.join(self.ddir, BUS_EXTRACT_FILE)
                rail_path = os.path.join(self.ddir, RAIL_EXTRACT_FILE)
                if os.path.isfile(bus_path) and os.path.isfile(rail_path):
                    # rename the extracted files
                    os.rename(rail_path, os.path.join(self.ddir, RAIL_FILE))
                    os.rename(bus_path, os.path.join(self.ddir, BUS_FILE))

                    rail_good = bus_good = False
                    if self.verify(BUS_FILE):
                        bus_good = True
                    else:
                        LOG.warn('SEPTA bus GTFS verification failed.')
                        return False
                    if self.verify(RAIL_FILE):
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
