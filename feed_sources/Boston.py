"""Fetch Massacheusetts Bay Transportation Authority (Boston) feed."""
import logging

from FeedSource import FeedSource

URL = 'http://www.mbta.com/uploadedfiles/MBTA_GTFS.zip'

LOG = logging.getLogger(__name__)


class Boston(FeedSource):
    """Fetch MBTA feed."""
    def __init__(self):
        super(Boston, self).__init__()
        self.urls = {'boston.zip': URL}
