#!/usr/bin/env python
"""Command line interface for fetching GTFS."""
import argparse
import logging
import sys

from FeedSource import FeedSource
import feed_sources
# import all the available feed sources
# pylint: disable=I0011,wildcard-import
from feed_sources import *

logging.basicConfig()
LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)

def fetch_all():
    """Fetch from all FeedSources in the feed_sources directory."""
    LOG.info('Going to fetch feeds from sources: %s', feed_sources.__all__)
    for src in feed_sources.__all__:
        mod = getattr(feed_sources, src)
        # expect a class with the same name as the module; instantiate and fetch its feeds
        klass = getattr(mod, src)
        if issubclass(klass, FeedSource):
            inst = klass()
            inst.fetch()
        else:
            LOG.warn('Skipping class %s, which does not subclass FeedSource.', klass.__name__)

def main():
    """Main entry point for command line interface."""
    parser = argparse.ArgumentParser(description='Fetch GTFS feeds and validate them.')
    parser.add_argument('--get-nj', action='store_true',
                        help='Fetch NJ TRANSIT (requires username and password; default: false)')
    parser.add_argument('--nj-username', action='store_const', const='',
                        help='Username for NJ TRANSIT developer account (optional)')
    parser.add_argument('--nj-password', action='store_const', const='',
                        help='Password for NJ TRANSIT developer account (optional)')

    args = parser.parse_args()
    if args.get_nj and (not args.nj_username or not args.nj_password):
        LOG.warn('--nj-username and --nj-password are required to fetch NJ TRANSIT feeds.')
        sys.exit(1)

    # should specify --get-nj when email alert received that new download available
    #fetcher = FeedFetcher(get_nj=args.get_nj,
    #                      nj_username=args.nj_username,
    #                      nj_pass=args.nj_password)
    #fetcher.fetch_all()
    fetch_all()

if __name__ == '__main__':
    main()


# TODO: deal with NJ
#self.get_nj = get_nj # whether to fetch from NJ TRANSIT or not
#        self.nj_payload = {'userName': nj_username, 'password': nj_pass}
#        if get_nj and (not nj_username or not nj_pass):
#            self.get_nj = False
#            print("Cannot fetch from NJ TRANSIT without nj_username and nj_pass specified.")
