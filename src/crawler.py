#!/usr/bin/env python

from __future__ import print_function # for print()
from crawler import data
import argparse
import sys

def main(args):
    """Main routine

    \param args Instance of argparse.ArgumentParser
    \return Integer indicating the return code"""

    success = True
    # main actions (mutual exclusive)
    if args.crawl:
        print("Starting to crawl result pages")
        db = data.openDatabase()
        success = data.crawlResultpages(db)
    elif args.extend:
        print("Starting to augment tracks")
        db = data.openDatabase()
        success = data.augmentTracks(db)
    elif args.statistics:
        print("Printing statistics")
        db = data.openDatabase()
        success = data.printStatistics(db)
    elif args.prune:
        print("Starting pruning database")
        db = data.openDatabase()
        success = data.pruneDatabase(db)
    else:
        print("No action specified")
        success = False

    return 0 if success else 1

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(
        prog='crawler',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='XML Crawler for gpsies.com',
        epilog="""Example URLs:
  www.gpsies.org/api.do?key=YOUR_API_KEY&lat=51&lon=10&perimeter=80&limit=20&trackTypes=jogging&filetype=kml"""
    )

    # options
    parser.add_argument('-c', '--crawl', action='store_true',
        help='Crawl from gpsies.com, parse result pages')
    parser.add_argument('-e', '--extend', action='store_true',
        help='Crawl from gpsies.com, extend non-augmented tracks with track details')
    parser.add_argument('-s', '--statistics', action='store_true',
        help='Print database statistics')
    parser.add_argument('-p', '--prune', action='store_true',
        help='Clear database, remove all non-augmented tracks')
    args = parser.parse_args()

    rc = main(args)
    sys.exit(rc)
