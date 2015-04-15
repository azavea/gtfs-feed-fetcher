"""Fetch Delaware First State feed."""
from FeedSource import FeedSource

URL = 'http://dartfirststate.com/information/routes/gtfs_data/dartfirststate_de_us.zip'

class Delaware(FeedSource):
    """Fetch DART feed."""
    def __init__(self):
        super(Delaware, self).__init__()
        self.urls = {'dart.zip': URL}
