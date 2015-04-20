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
LOG.setLevel(logging.INFO)

NJ_TRANSIT_CLASS = 'NJTransit'

def fetch_all(get_nj, nj_username, nj_password, sources=None):
    """Fetch from all FeedSources in the feed_sources directory."""
    statuses = {}  # collect the statuses for all the files

    # make a copy of the list of all modules in feed_sources;
    # default to use all of them (excluding NJ, if not requested)
    if not sources:
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
            statuses.update(inst.status)
        else:
            LOG.info('Skipping NJ data fetch.')
    elif get_nj:
        LOG.warn('No NJ TRANSIT class defined! Skipping fetch.')

    for src in sources:
        LOG.debug('Going to start fetch for %s...', src)
        try:
            mod = getattr(feed_sources, src)
            # expect a class with the same name as the module; instantiate and fetch its feeds
            klass = getattr(mod, src)
            if issubclass(klass, FeedSource):
                inst = klass()
                inst.fetch()
                statuses.update(inst.status)
            else:
                LOG.warn('Skipping class %s, which does not subclass FeedSource.', klass.__name__)
        except AttributeError:
            LOG.error('Skipping feed %s, which could not be found.', src)

    # remove last check key set at top level of each status dictionary
    if statuses.has_key('last_check'):
        del statuses['last_check']

    for file_name in statuses:
        stat = statuses[file_name]
        if stat.has_key('error'):
            LOG.error('Error processing %s: %s', file_name, stat['error'])
            continue
        msg = ''
        msg += 'is new; ' if stat['is_new'] else 'is not new; '
        msg += 'is valid; ' if stat['is_valid'] else 'is not valid; '
        msg += 'is current.' if stat['is_current'] else 'is not current.'
        msg += ' Newly effective!' if stat.get('newly_effective') else ''

        LOG.info('File %s %s', file_name, msg)
    LOG.info('All done!')

def main():
    """Main entry point for command line interface."""
    parser = argparse.ArgumentParser(description='Fetch GTFS feeds and validate them.')
    parser.add_argument('--get-nj', action='store_true',
                        help='Fetch NJ TRANSIT (requires username and password; default: false)')
    parser.add_argument('--nj-username',
                        help='Username for NJ TRANSIT developer account (optional)')
    parser.add_argument('--nj-password',
                        help='Password for NJ TRANSIT developer account (optional)')
    parser.add_argument('--feeds',
                        help='Comma-separated list of feeds to get (optional; default: all)')
    parser.add_argument('--verbose', '-v', action='count')

    args = parser.parse_args()
    if args.verbose:
        LOG.setLevel(logging.DEBUG)

    if args.get_nj and (not args.nj_username or not args.nj_password):
        LOG.warn('--nj-username and --nj-password are required to fetch NJ TRANSIT feeds.')
        sys.exit(1)

    # should specify --get-nj when email received saying new download available
    if args.feeds:
        sources = args.feeds.split(',')
        fetch_all(args.get_nj, args.nj_username, args.nj_password, sources=sources)
    else:
        fetch_all(args.get_nj, args.nj_username, args.nj_password)

if __name__ == '__main__':
    main()
