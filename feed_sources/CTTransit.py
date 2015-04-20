"""Fetch CT Transit (Connecticut) feeds."""
import logging

from FeedSource import FeedSource

LOG = logging.getLogger(__name__)

BASE_URL = 'http://www.cttransit.com/uploads_GTFS/'
SHORELINE_EAST_URL = 'http://www.shorelineeast.com/google_transit.zip'


class CTTransit(FeedSource):
    """Fetch PATH feed."""
    def __init__(self):
        super(CTTransit, self).__init__()
        # feeds for Hartford, New Haven, Stamford, Waterbury, New Britain, Meridien,
        # and Shore Line East.  Shore Line East has its own URL.
        ct_suffixes = {'Hartford': 'ha', 'New Haven': 'nh', 'Stamford': 'stam',
                       'Waterbury': 'wat', 'New Britain': 'nb', 'Meridien': 'me'}

        urls = {}
        for sfx in ct_suffixes:
            url = '%sgoogle%s_transit.zip' % (BASE_URL, ct_suffixes[sfx])
            filename = 'ct_%s.zip' % ct_suffixes[sfx]
            urls[filename] = url

        urls['ct_shoreline_east.zip'] = SHORELINE_EAST_URL
        self.urls = urls
