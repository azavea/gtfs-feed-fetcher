"""Fetch Monroe Country Transit Authority (Pocono Pony) feed.

Looks like GTFSExchange is the authoritative source for this feed.
"""
import logging

from FeedSource import FeedSource

URL = 'http://www.gtfs-data-exchange.com/agency/monroe-county-transit-authority/latest.zip'

LOG = logging.getLogger(__name__)


class Pocono(FeedSource):
    """Fetch Monroe County feed."""
    def __init__(self):
        super(Pocono, self).__init__()
        self.urls = {'pocono.zip': URL}
