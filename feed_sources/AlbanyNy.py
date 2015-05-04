"""Fetch Capital District Transportation Authority (Albany, New York) feed."""
import logging

from FeedSource import FeedSource

URL = 'http://www.cdta.org/schedules/google_transit.zip'

LOG = logging.getLogger(__name__)


class AlbanyNy(FeedSource):
    """Fetch CDTA feed."""
    def __init__(self):
        super(AlbanyNy, self).__init__()
        self.urls = {'albany_ny.zip': URL}
