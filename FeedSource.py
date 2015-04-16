"""Defines base class for feed(s) from an agency.

To add a new feed, add a subclass of this to the `feed_sources` directory.
"""
from datetime import datetime
import logging
import os
import pickle
import subprocess
import zipfile

import requests

LOG = logging.getLogger(__name__)

# format time checks like last-modified header
TIMECHECK_FMT = '%a, %d %b %Y %H:%M:%S GMT'

class FeedSource(object):
    """Base class for a GTFS source. Class and module names are expected to match.

    Subclass this class and:
        - set class :urls: to a dictionary of { filename: url }:
            :filename: is the what the feed will be saved as (should end in .zip)
            :url: is the URL where the feed will be downloaded from
        - override :fetch: method as necessary to fetch feeds for the agency.
    """
    def __init__(self, ddir=os.path.join(os.getcwd(), 'gtfs')):
        # set properties
        self._ddir = ddir
        self._urls = None
        self._new_use = []
        self._timecheck = {}
        self._timecheck_file = os.path.join(self.ddir, self.__class__.__name__ + '.p')
        # load time check file
        self.load_timecheck()

    @property
    def ddir(self):
        """Directory to download feeds into."""
        return self._ddir
    @ddir.setter
    def ddir(self, value):
        self._ddir = value

    @property
    def urls(self):
        """Set to a dictionary of { filename: url } for agency"""
        return self._urls
    @urls.setter
    def urls(self, value):
        self._urls = value

    @property
    def new_use(self):
        """List of new feeds successfully downloaded and validated."""
        return self._new_use
    @new_use.setter
    def new_use(self, value):
        self._new_use = value

    @property
    def timecheck(self):
        """Time checks for GTFS fetches."""
        return self._timecheck
    @timecheck.setter
    def timecheck(self, value):
        self._timecheck = value

    @property
    def timecheck_file(self):
        """Pickle file where time checks are stored.

        Defaults to name file after class, and store it in :ddir:."""
        return self._timecheck_file
    @timecheck_file.setter
    def timecheck_file(self, value):
        self._timecheck_file = value


    def fetch(self):
        """Modify this method in sub-class for importing feed(s) from agency.

        By default, loops over given URLs, checks the last-modified header to see if a new
        download is available, streams the download if so, and verifies the new GTFS.
        """
        if self.urls:
            for filename in self.urls:
                url = self.urls.get(filename)
                if self.fetchone(filename, url):
                    self.write_timecheck()
        else:
            LOG.warn('No URLs to download for %s.', self.__class__.__name__)

    def load_timecheck(self):
        """Read in pickled log of last times files were downloaded."""
        if os.path.isfile(self.timecheck_file):
            with open(self.timecheck_file, 'rb') as tcf:
                self.timecheck = pickle.load(tcf)
                LOG.debug('Loaded time check file.')
            if self.timecheck.has_key('last_check'):
                last_fetch = self.timecheck.get('last_check')
                LOG.info('Last fetch at: %s', last_fetch)
                timedelta = datetime.now() - last_fetch
                LOG.info('Time since last fetch: %s', timedelta)
        else:
            LOG.debug('Will create new time check file.')

        self.timecheck['last_check'] = datetime.now()

    def write_timecheck(self):
        """Write pickled log of last times files were downloaded."""
        LOG.debug('Downloading finished.  Writing time check file %s...', self.timecheck_file)
        with open(self.timecheck_file, 'wb') as tcf:
            pickle.dump(self.timecheck, tcf)
            LOG.debug('Time check written to %s.', self.timecheck_file)

    def fetchone(self, file_name, url, verify=True, **stream):
        """Download and validate a single feed."""
        if self.download(file_name, url, **stream):
            if verify:
                if self.verify(file_name):
                    LOG.info('GTFS verification succeeded.')
                    self.new_use.append(file_name)
                    return True
                else:
                    LOG.error('GTFS verification failed.')
                    return False
            else:
                LOG.debug('Skipping GTFS verification in fetch_and_validate.')
                # not adding to new_use here; do elsewhere
                return True
        else:
            return False

    def verify(self, file_name):
        """Verify downloaded file looks like a good GTFS."""
        # file_name is local to download directory
        downloaded_file = os.path.join(self.ddir, file_name)
        if not os.path.isfile(downloaded_file):
            LOG.error('File %s not found; cannot verify it.', downloaded_file)
            return False

        LOG.info('Validating feed in %s...', file_name)
        try:
            process_cmd = ['feedvalidator.py',
                           '--output=CONSOLE',
                           '-m',
                           '-n',
                           downloaded_file]

            # Process returns failure on warnings, which most feeds have;
            # we will return success here if there are only warnings and no errors.
            process = subprocess.Popen(process_cmd, stdout=subprocess.PIPE)
            out = process.communicate()
            res = out[0].split('\n')
            errct = res[-2:-1][0] # output line with count of errors/warnings
            if errct.find('error') > -1:
                LOG.error('Feed validator found errors in %s: %s.', file_name, errct)
                return False
            elif out[0].find('this feed is in the future,') > -1:
                LOG.warn('Feed validator found GTFS not in service until future for %s.', file_name)
                return False
            else:
                if errct.find('successfully') > -1:
                    LOG.info('Feed %s looks great:  %s.', file_name, errct)
                else:
                    # have warnings
                    LOG.info('Feed %s looks ok:  %s.', file_name, errct[7:])
                return True
        except IndexError:
            LOG.error('Could not parse feed validation results for %s: %s', file_name, out)
            return False

        LOG.error('How did we get here?  Verifying %s.', file_name)
        return False # should have returned above

    def check_header_newer(self, url, file_name):
        """return 1 if newer file available to download;
           return 0 if info missing;
           return -1 if current file is most recent."""
        if self.timecheck.has_key(file_name):
            last_info = self.timecheck.get(file_name)
            hdr = requests.head(url)
            hdr = hdr.headers
            if hdr.get('last-modified'):
                last_mod = hdr.get('last-modified')
                if last_mod == last_info:
                    LOG.info('No new download available for %s.', file_name)
                    return -1
                else:
                    LOG.info('New download available for %s.', file_name)
                    LOG.info('Last downloaded: %s.', last_info)
                    LOG.info('New download posted: %s', last_mod)
                    return 1
            else:
                # should try to find another way to check for new feeds if header not set
                LOG.debug('No last-modified header set for %s download link.', file_name)
                return 0
        else:
            LOG.debug('Time check entry for %s not found.', file_name)
            return 0

    def download(self, file_name, url, do_stream=True, session=None):
        """Download feed."""
        LOG.debug('In get_stream to get file %s from URL %s.', file_name, url)
        if self.check_header_newer(url, file_name) == -1:
            return False
        # file_name is local to download directory
        file_path = os.path.join(self.ddir, file_name)
        LOG.info('Getting file %s...', file_path)
        if not session:
            request = requests.get(url, stream=do_stream)
        else:
            request = session.get(url, stream=do_stream)

        if request.ok:
            with open(file_path, 'wb') as download_file:
                if do_stream:
                    for chunk in request.iter_content():
                        download_file.write(chunk)
                else:
                    download_file.write(request.content)

            info = os.stat(file_path)
            if info.st_size < 10000:
                # file smaller than 10K; may not be a GTFS
                LOG.warn('Download for %s is only %s bytes.', file_path, str(info.st_size))
            if not zipfile.is_zipfile(file_path):
                LOG.error('Bad download for %s.', file_path)
                print('Download for %s is not a zip file.', file_path)
                return False
            if request.headers.get('last-modified'):
                self.timecheck[file_name] = request.headers.get('last-modified')
            else:
                self.timecheck[file_name] = datetime.utcnow().strftime(TIMECHECK_FMT)
            LOG.info('Download completed successfully.')
            return True
        else:
            LOG.error('Download failed for %s.', file_name)
        return False
