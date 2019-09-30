"""Fetch CT Transit (Connecticut) feeds."""
import logging

from FeedSource import FeedSource

LOG = logging.getLogger(__name__)

BASE_URL = 'http://www.cttransit.com/sites/default/files/gtfs/googlect_transit.zip'
SHORELINE_EAST_URL = 'http://www.shorelineeast.com/google_transit.zip'
HARTFORD_URL = 'http://www.hartfordline.com/files/gtfs/gtfs.zip'


class CTTransit(FeedSource):
    """Fetch PATH feed."""
    def __init__(self):
        super(CTTransit, self).__init__()
        self.urls = {
            'ct_transit.zip': BASE_URL,
            'ct_shoreline_east.zip': SHORELINE_EAST_URL,
            'ct_hartford_rail.zip': HARTFORD_URL
        }
