"""Fetch official PATCO feed."""

from datetime import datetime
import logging
import requests

from FeedSource import FeedSource, TIMECHECK_FMT

URL = 'https://addtransit.com/gtfs/Patco/PortAuthorityTransitCorporation.zip'
FILE_NAME = 'patco.zip'

LOG = logging.getLogger(__name__)


class Patco(FeedSource):
    """Fetch official PATCO feed."""
    def __init__(self):
        super(Patco, self).__init__()
        self.urls = {'patco.zip': URL}

