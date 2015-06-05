#!/usr/bin/env python

from distutils.core import setup

setup(name='GtfsFetcher',
      version='0.1.0',
      description='Download, validate, and manage GTFS transit feeds',
      author='Kathryn Killebrew',
      author_email='kathryn.killebrew@gmail.com',
      url='https://github.com/azavea/gtfs-feed-fetcher',
      py_modules=['fetch_feeds', 'extend_effective_dates', 'check_status'])
