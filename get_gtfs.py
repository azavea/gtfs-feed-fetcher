#!/usr/bin/env python
import argparse
import sys

from FeedFetcher import FeedFetcher

def main():
    parser = argparse.ArgumentParser(description='Fetch GTFS feeds and validate them.')
    parser.add_argument('--get-nj', action='store_true',
                        help='Fetch NJ TRANSIT (requires username and password; default: false)')
    parser.add_argument('--nj-username', action='store_const', const='',
                        help='Username for NJ TRANSIT developer account (optional)')
    parser.add_argument('--nj-password', action='store_const', const='',
                        help='Password for NJ TRANSIT developer account (optional)')

    args = parser.parse_args()
    if (args.get_nj and (not args.nj_username or not args.nj_password)):
        print('--nj-username and --nj-password are required to fetch NJ TRANSIT feeds.')
        sys.exit(1)

    # should specify --get-nj when email alert received that new download available
    fetcher = FeedFetcher(get_nj=args.get_nj,
                          nj_username=args.nj_username,
                          nj_pass=args.nj_password)
    fetcher.fetch()

if __name__ == '__main__':
    main()
