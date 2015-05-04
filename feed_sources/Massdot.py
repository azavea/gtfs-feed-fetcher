"""Fetch Massacheusetts Department of Transportation feeds.

MassDOT supplies the feeds for MA not covered by MBTA (Boston's transit authority).
http://www.massdot.state.ma.us/DevelopersData.aspx
"""
import logging

from FeedSource import FeedSource

BASE_URL = 'http://www.massdot.state.ma.us/Portals/0/docs/developers/'

LOG = logging.getLogger(__name__)


class Massdot(FeedSource):
    """Fetch MassDOT (MA, non-Boston) feeds."""
    def __init__(self):
        super(Massdot, self).__init__()

        berkshire_url = '%sbrta_google_transit.zip' % BASE_URL
        brockton_url = '%sbat_google_transit.zip' % BASE_URL
        cape_ann_url = '%scata_google_transit.zip' % BASE_URL
        cape_cod_url = '%sccrta_google_transit.zip' % BASE_URL
        franklin_url = '%sfrta_google_transit.zip' % BASE_URL
        attleboro_url = '%sgatra_google_transit.zip' % BASE_URL
        lowell_url = '%slrta_google_transit.zip' % BASE_URL
        merrimack_url = '%smvrta_google_transit.zip' % BASE_URL
        metrowest_url = '%smwrta_google_transit.zip' % BASE_URL
        montachusett_url = '%smart_google_transit.zip' % BASE_URL
        nantucket_url = '%snrta_google_transit.zip' % BASE_URL
        pioneer_valley_url = 'http://www.pvta.com/g_trans/google_transit.zip'
        southeastern_url = '%ssrta_google_transit.zip' % BASE_URL
        vineyard_url = '%svta_google_transit.zip' % BASE_URL
        worchester_url = '%swrta_google_transit.zip' % BASE_URL
        ma_ferry_url = '%sferries_google_transit.zip' % BASE_URL

        # private bus services; these feeds tend to have validation issues
        bloom_url = '%sBloom_google_transit.zip' % BASE_URL
        boston_express_url = '%sboston_express_google_transit.zip' % BASE_URL
        coach_bus_url = '%scoach_google_transit.zip' % BASE_URL
        dattco_url = '%sdattco_google_transit.zip' % BASE_URL
        peter_pan_url = '%speter_pan_google_transit.zip' % BASE_URL
        plymouth_brockton_railway_url = '%sPB_google_transit.zip' % BASE_URL
        yankee_url = '%syankee_google_transit.zip' % BASE_URL

        self.urls = {
            'berkshire.zip': berkshire_url,
            'brockton.zip': brockton_url,
            'cape_ann.zip': cape_ann_url,
            'cape_cod.zip': cape_cod_url,
            'franklin.zip': franklin_url,
            'attleboro.zip': attleboro_url,
            'lowell.zip': lowell_url,
            'merrimack.zip': merrimack_url,
            'metrowest.zip': metrowest_url,
            'montachusett.zip': montachusett_url,
            'nantucket.zip': nantucket_url,
            'pioneer_valley.zip': pioneer_valley_url,
            'southeastern_ma.zip': southeastern_url,
            'vineyard_ma.zip': vineyard_url,
            'worchester.zip': worchester_url,
            'ma_ferries.zip': ma_ferry_url,
            'bloom_ma.zip': bloom_url,
            'boston_express.zip': boston_express_url,
            'coach_bus_ma.zip': coach_bus_url,
            'dattco_ma.zip': dattco_url,
            'peter_pan_ma.zip': peter_pan_url,
            'plymouth_brockton_rail.zip': plymouth_brockton_railway_url,
            'yankee_ma.zip': yankee_url
        }
