"""Fetch California feeds."""
import logging

from FeedSource import FeedSource


LOG = logging.getLogger(__name__)


class California(FeedSource):
    """Fetch various feeds in California."""
    def __init__(self):
        super(California, self).__init__()

        self.urls = {
            'amador.zip': 'http://data.trilliumtransit.com/gtfs/amador-ca-us/amador-ca-us.zip',
            'bart.zip': 'http://www.bart.gov/dev/schedules/google_transit.zip',
            'beartransit.zip': 'http://data.trilliumtransit.com/gtfs/beartransit-ca-us/beartransit-ca-us.zip',
            'beaumont.zip': 'http://data.trilliumtransit.com/gtfs/beaumont-ca-us/beaumont-ca-us.zip',
            'bigbear.zip': 'http://data.trilliumtransit.com/gtfs/bigbear-ca-us/bigbear-ca-us.zip',
            'calaveras.zip': 'http://data.trilliumtransit.com/gtfs/calaveras-ca-us/calaveras-ca-us.zip',
            'caltrain.zip': 'http://www.caltrain.com/Assets/GTFS/caltrain/GTFS-Caltrain-Devs-10-05-2014.zip',
            'central_contra_costa.zip': 'http://cccta.org/GTFS/google_transit.zip',
            'corona.zip': 'http://data.trilliumtransit.com/gtfs/corona-ca-us/corona-ca-us.zip',
            'davis_unitrans.zip': 'http://iportal.sacrt.com/GTFS/Unitrans/google_transit.zip',
            'eastern_sierra.zip': 'http://data.trilliumtransit.com/gtfs/easternsierra-ca-us/easternsierra-ca-us.zip',
            'escalon.zip': 'http://data.trilliumtransit.com/gtfs/escalon-ca-us/escalon-ca-us.zip',
            'fairfield.zip': 'http://data.trilliumtransit.com/gtfs/fairfield-ca-us/fairfield-ca-us.zip',
            'fresno.zip': 'http://data.trilliumtransit.com/gtfs/fresnocounty-ca-us/fresnocounty-ca-us.zip',
            'golden_empire.zip': 'http://www.getbus.org/googletransit/google_transit.zip',
            'humboldt.zip': 'http://data.trilliumtransit.com/gtfs/humboldtcounty-ca-us/humboldtcounty-ca-us.zip',
            'irvine.zip': 'http://irvineshuttle.net/files/managed/Document/70/google_transit.zip',
            'kerncounty.zip': 'http://data.trilliumtransit.com/gtfs/kerncounty-ca-us/kerncounty-ca-us.zip',
            'la_county_metro.zip': 'http://developer.metro.net/gtfs/google_transit.zip',
            'ladot.zip': 'http://www.gtfs-data-exchange.com/agency/ladot/latest.zip',
            'lagunabeach.zip': 'http://data.trilliumtransit.com/gtfs/lagunabeach-ca-us/lagunabeach-ca-us.zip',
            'lake_tahoe.zip': 'http://data.trilliumtransit.com/gtfs/laketahoe-ca-us/laketahoe-ca-us.zip',
            'lassen.zip': 'http://data.trilliumtransit.com/gtfs/lassen-ca-us/lassen-ca-us.zip',
            'madera.zip': 'http://data.trilliumtransit.com/gtfs/madera-ca-us/madera-ca-us.zip',
            'marin.zip': 'http://www.marintransit.org/data/google_transit.zip',
            'mendocino.zip': 'http://data.trilliumtransit.com/gtfs/mendocino-ca-us/mendocino-ca-us.zip',
            'merced.zip': 'http://data.trilliumtransit.com/gtfs/mercedthebus-ca-us/mercedthebus-ca-us.zip',
            'metrolink.zip': 'http://www.metrolinktrains.com/content/google_transit.zip',
            'modesto.zip': 'http://data.trilliumtransit.com/gtfs/modesto-ca-us/modesto-ca-us.zip',
            'north_san_diego.zip': 'http://www.gonctd.com/google_transit.zip',
            'orange.zip': 'http://www.octa.net/current/google_transit.zip',
            'palm_springs.zip': 'http://www.sunline.org/transit/google_transit.zip',
            'palos_verdes.zip': 'http://data.trilliumtransit.com/gtfs/pvpta-ca-us/pvpta-ca-us.zip',
            'plumas.zip': 'http://data.trilliumtransit.com/gtfs/plumas-ca-us/plumas-ca-us.zip',
            'redding.zip': 'http://data.trilliumtransit.com/gtfs/redding-ca-us/redding-ca-us.zip',
            'rio_vista.zip': 'http://data.trilliumtransit.com/gtfs/riovista-ca-us/riovista-ca-us.zip',
            'roseville.zip': 'http://iportal.sacrt.com/GTFS/Roseville/google_transit.zip',
            'sacramento.zip': 'http://iportal.sacrt.com/GTFS/SRTD/google_transit.zip',
            'sage_state.zip': 'http://www.gtfs-data-exchange.com/agency/sage-stage/latest.zip',
            'san_benito.zip': 'http://data.trilliumtransit.com/gtfs/sanbenito-ca-us/sanbenito-ca-us.zip',
            'san_bernadino.zip': 'http://www.omnitrans.org/google/google_transit.zip',
            'san_diego_mts.zip': 'http://www.sdmts.com/google_transit_files/google_transit.zip',
            'san_joaquin.zip': 'http://sanjoaquinrtd.com/RTD-GTFS/RTD-GTFS.zip',
            'san_luis_obispo.zip': 'http://www.gtfs-data-exchange.com/agency/san-luis-obispo-regional-transit-authority/latest.zip',
            'santa_cruz.zip': 'http://scmtd.com/google_transit/google_transit.zip',
            'sfbay_ferries.zip': 'http://data.trilliumtransit.com/gtfs/sfbay-ferries-ca-us/sfbay-ferries-ca-us.zip',
            'sfmta.zip': 'http://archives.sfmta.com/transitdata/google_transit.zip',
            'siskiyou.zip': 'http://data.trilliumtransit.com/gtfs/siskiyou-ca-us/siskiyou-ca-us.zip',
            'sonoma.zip': 'http://data.trilliumtransit.com/gtfs/sonomacounty-ca-us/sonomacounty-ca-us.zip',
            'south_county.zip': 'http://www.gtfs-data-exchange.com/agency/south-county-area-transit/latest.zip',
            'stanislaus.zip': 'http://data.trilliumtransit.com/gtfs/stanislaus-ca-us/stanislaus-ca-us.zip',
            'tehama.zip': 'http://data.trilliumtransit.com/gtfs/tehama-ca-us/tehama-ca-us.zip',
            'thousandoaks.zip': 'http://www.toaks.org/GoogleTransit/thousandoaks/google_transit.zip',
            'torrance.zip': 'http://www.torranceca.gov/TransitFeed/google_transit.zip',
            'trinity.zip': 'http://data.trilliumtransit.com/gtfs/trinity-ca-us/trinity-ca-us.zip',
            'victorville.zip': 'http://data.trilliumtransit.com/gtfs/victorville-ca-us/victorville-ca-us.zip',
            'western_nevada.zip': 'http://gis.nevcounty.net/GTFS/GTFS.zip',
            'yolo.zip': 'http://iportal.sacrt.com/GTFS/Yolobus/google_transit.zip',
            'yosemite.zip': 'http://data.trilliumtransit.com/gtfs/yosemite-ca-us/yosemite-ca-us.zip',
            'yuba.zip': 'http://data.trilliumtransit.com/gtfs/yubasutter-ca-us/yubasutter-ca-us.zip'
 }


    def fetch(self):
        for filename in self.urls:
            url = self.urls.get(filename)
            self.fetchone(filename, url):
            self.write_status()
