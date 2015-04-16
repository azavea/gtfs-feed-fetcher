"""Fetch CT Transit (Connecticut) feeds."""
import logging

from FeedSource import FeedSource

LOG = logging.getLogger(__name__)


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
            url = 'http://www.cttransit.com/uploads_GTFS/google%s_transit.zip' % ct_suffixes[sfx]
            filename = 'ct_%s.zip' % ct_suffixes[sfx]
            urls[filename] = url

        urls['ct_shoreline_east'] = 'http://www.shorelineeast.com/google_transit.zip'
        self.urls = urls
