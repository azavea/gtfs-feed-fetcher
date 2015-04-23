"""Fetch NJ TRANSIT bus and rail feeds.

Requires username and password to log in first.
Cannot check for whether a feed is new or not, so only call to fetch this one once
an email is sent to the developer account saying new feeds are available.
"""
import logging

import requests

from FeedSource import FeedSource


LOG = logging.getLogger(__name__)

LOGIN_URL = 'https://www.njtransit.com/mt/mt_servlet.srv?hdnPageAction=MTDevLoginSubmitTo'
URL = 'https://www.njtransit.com/mt/mt_servlet.srv?hdnPageAction=MTDevResourceDownloadTo&Category='


class NJTransit(FeedSource):
    """Create session to fetch NJ TRANSIT feed bus and rail feeds."""
    def __init__(self):
        super(NJTransit, self).__init__()
        self.urls = {'nj_rail.zip': URL + 'rail', 'nj_bus.zip': URL + 'bus'}
        self.nj_payload = {} # need to set username and password in this to log in

    def fetch(self):
        """Fetch NJ TRANSIT bus and rail feeds.

        First logs on to create session before fetching and validating downloads.
        """
        for filename in self.urls:
            session = requests.Session()
            login = session.post(LOGIN_URL, data=self.nj_payload)
            if login.ok:
                LOG.debug('Logged in to NJ TRANSIT successfully.')
                url = self.urls.get(filename)
                if self.fetchone(filename, url, session=session):
                    self.write_status()
            else:
                LOG.error('Failed to log in to NJ TRANSIT. Response status: %s: %s.',
                          login.status_code, login.reason)
            session.close()
