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

NJ_TRANSIT_CLASS = 'NJTransit'

def fetch_all(get_nj, nj_username, nj_password):
    """Fetch from all FeedSources in the feed_sources directory."""
    # make a copy
    sources = list(feed_sources.__all__)
    LOG.info('Going to fetch feeds from sources: %s', sources)

    # NJ TRANSIT requires some special handling; do that here
    if NJ_TRANSIT_CLASS in sources:
        sources.remove(NJ_TRANSIT_CLASS)
        if get_nj:
            LOG.debug('Going to start fetch for %s...', NJ_TRANSIT_CLASS)
            mod = getattr(feed_sources, NJ_TRANSIT_CLASS)
            klass = getattr(mod, NJ_TRANSIT_CLASS)
            inst = klass()
            inst.nj_payload = {'userName': nj_username, 'password': nj_password}
            inst.fetch()
        else:
            LOG.info('Skipping NJ data fetch.')
    elif get_nj:
        LOG.warn('No NJ TRANSIT class defined! Skipping fetch.')

    for src in sources:
        LOG.debug('Going to start fetch for %s...', src)
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
    parser.add_argument('--nj-username',
                        help='Username for NJ TRANSIT developer account (optional)')
    parser.add_argument('--nj-password',
                        help='Password for NJ TRANSIT developer account (optional)')

    args = parser.parse_args()
    if args.get_nj and (not args.nj_username or not args.nj_password):
        LOG.warn('--nj-username and --nj-password are required to fetch NJ TRANSIT feeds.')
        sys.exit(1)

    # should specify --get-nj when email received saying new download available
    fetch_all(args.get_nj, args.nj_username, args.nj_password)

if __name__ == '__main__':
    main()
