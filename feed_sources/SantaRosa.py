"""Fetch Santa Rosa, CA feed via FTP."""
from datetime import datetime
import logging
import os
import urllib

from FeedSource import FeedSource, TIMECHECK_FMT


LOG = logging.getLogger(__name__)


class SantaRosa(FeedSource):
    """Fetch Santa Rosa, CA feed via FTP."""
    def __init__(self):
        super(SantaRosa, self).__init__()

        self.urls = {
            'santa_rosa.zip': 'ftp://ftp.ci.santa-rosa.ca.us/SantaRosaCityBus/google_transit.zip'
        }

    def fetch(self):
        for filename in self.urls:
            try:
                # download file into download directory
                download_path = os.path.join(self.ddir, filename)
                urllib.urlretrieve(self.urls.get(filename), download_path)
                # TODO: does FTP preserve post date?
                posted_date = datetime.utcnow().strftime(TIMECHECK_FMT)
                self.set_posted_date(filename, posted_date)
                if self.verify(filename):
                    LOG.info('GTFS verification succeeded.')
                    self.write_status()
                    return True
                else:
                    LOG.error('GTFS verification failed.')
                    self.write_status()
                    return False
            except IOError as ex:
                msg = str(ex)
                LOG.error('Error downloading %s: %s', filename, msg)
                self.set_error(filename, msg)
                return False
