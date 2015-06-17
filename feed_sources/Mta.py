"""Fetch MTA (New York City) feeds."""
import logging

from FeedSource import FeedSource

BASE_URL = 'http://web.mta.info/developers/data/'

LOG = logging.getLogger(__name__)


class Mta(FeedSource):
    """Fetch MTA (NYC) feeds."""
    def __init__(self):
        super(Mta, self).__init__()

        nyc_sub_url = '%snyct/subway/google_transit.zip' % BASE_URL
        bronx_bus_url = '%snyct/bus/google_transit_bronx.zip' % BASE_URL
        brooklyn_bus_url = '%snyct/bus/google_transit_brooklyn.zip' % BASE_URL
        manhattan_bus_url = '%snyct/bus/google_transit_manhattan.zip' % BASE_URL
        queens_bus_url = '%snyct/bus/google_transit_queens.zip' % BASE_URL
        staten_bus_url = '%snyct/bus/google_transit_staten_island.zip' % BASE_URL
        lirr_url = '%slirr/google_transit.zip' % BASE_URL
        metro_north_url = '%smnr/google_transit.zip' % BASE_URL
        busco_url = '%sbusco/google_transit.zip' % BASE_URL

        self.urls = {
            'nyc_subway.zip': nyc_sub_url,
            'bronx.zip': bronx_bus_url,
            'brooklyn.zip': brooklyn_bus_url,
            'manhattan.zip': manhattan_bus_url,
            'queens.zip': queens_bus_url,
            'staten.zip': staten_bus_url,
            'lirr.zip': lirr_url,
            'metro_north.zip': metro_north_url,
            'busco.zip': busco_url
        }

    def fetch(self):
        """MTA downloads do not stream."""
        for filename in self.urls:
            self.fetchone(filename, self.urls.get(filename), do_stream=False)
            self.write_status()
