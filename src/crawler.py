#!/usr/bin/env python

from __future__ import print_function # for print()
from crawler import data
from crawler.data import openDatabase
from crawler.parser import XmlParser
from lxml import etree
from shared import constants
from shared.interface import TrackInterface
from shared.util import log, options
import argparse
import sys
import time
import urllib2

def getApiKey():
    API_KEY = options.get('Common', 'API_KEY', )
    if not API_KEY:
        raise RuntimeError("API key not set: Set it in {0}".format(constants.USER_CONFIG))
    return API_KEY

def readUrl(url):
    if not url.startswith('http://'):
        url = 'http://' + url

    log.debug("Reading URL: {0}".format(url))

    start= time.time()
    f = urllib2.urlopen(url)
    content = f.read()
    end = time.time()
    log.debug("  took {0} ms".format(end-start))
    return content

def parseContent(content):
    parser = XmlParser()
    parser.parse(content)
    return parser.tree

def crawlResultpages(db):
    """Crawl from a specific set of result pages

    Fills the data base with non-augmented tracks

    \return True if successful, else False"""

    TRACKS_LIST_TEMPLATE = "{0}/api.do?key={1}&country={2}&limit=100&resultPage={3}"
    API_KEY = getApiKey()
    API_BASE_URL = options.get('Common', 'API_BASE_URL')
    MAX_DATABASE_SIZE = options.get('Common', 'MAX_DATABASE_SIZE')

    def getUrl(resultPage):
        url = TRACKS_LIST_TEMPLATE.format(
            API_BASE_URL, API_KEY, "DE", resultPage
        )
        return url

    iface = TrackInterface(db)

    numberOfTracks = 0
    resultPage = 142
    while numberOfTracks < MAX_DATABASE_SIZE:
        url = getUrl(resultPage)
        log.debug("Parsing URL: {0}".format(url))

        content = readUrl(url)
        tree = parseContent(content)

        tracksSearch = etree.XPath("//track")
        tracks = tracksSearch(tree)
        if len(tracks) == 0:
            break

        # add tracks to database
        iface.addTracks(tracks)
        log.debug("Added {0} tracks to the database".format(len(tracks)))
        resultPage += 1

        # print out number of tracks in db
        log.debug("Tracks in database: {0}".format(iface.getTrackCount()))

    return True

def augmentOneTrack(db, fileId):
    """Extend one specific track, by crawling gpsies.org once more

    @param fileId Track file ID
    @return True on success, False otherwise
    """

    TRACK_DETAILS_TEMPLATE = "{0}/api.do?key={1}&fileId={2}&trackDataLength=250"
    API_KEY = getApiKey()
    API_BASE_URL = options.get('Common', 'API_BASE_URL')

    def getUrl(fileId):
        url = TRACK_DETAILS_TEMPLATE.format(API_BASE_URL, API_KEY, fileId)
        return url

    url = getUrl(fileId)
    content = readUrl(url)

    tree = etree.fromstring(content)
    tracks = tree.xpath("//track") # should return exactly one track element
    assert(len(tracks) == 1)
    track = tracks[0]

    titles = tree.xpath("//track/title")
    assert(len(titles) == 1)
    title = etree.tostring(titles[0])
    if "API key required" in title:
        log.error("Title: {0}".format(title))
        raise RuntimeError("Fatal: API key broken? File ID: {0}".format(fileId))

    # transform to our database format
    success = data.transformTrack(track)
    if not success:
        log.debug("Failed to transform track to database format")
        return False

    # re-add node (with full details now)
    log.debug("Add track details for fileID: {0}".format(fileId))
    iface = TrackInterface(db)
    trackStr = etree.tostring(track)
    iface.addTrack(trackStr) # replaces
    return True

def augmentTracks(db):
    """Augment tracks that are already in the database"""

    iface = TrackInterface(db)
    tracks = iface.getNonAugmentedTracks()

    log.debug("Number of non-augmented tracks: {0}".format(iface.getNonAugmentedTrackCount()))

    iterations = 0
    for track in tracks:
        tree = etree.fromstring(track)
        fileId = tree.xpath("//fileId/text()")[0]

        log.debug("Finding track details for fileId: {0} (iteration {1})".format(fileId, iterations))
        augmentOneTrack(db, fileId)
        iterations += 1

    return True

def pruneDatabase(db):
    """Delete non-augmented tracks"""

    iface = TrackInterface(db)
    trackCount_old = iface.getTrackCount()
    tracks = iface.getNonAugmentedTracks()

    for track in tracks:
        iface.removeTrack(track)

    trackCount_new = iface.getTrackCount()
    removedTracksCount = trackCount_old - trackCount_new
    print("Removed tracks count: {0}".format(removedTracksCount))
    return True

def printStatistics(db):
    iface = TrackInterface(db)
    print("Number of non-augmented tracks: {0}".format(iface.getNonAugmentedTrackCount()))
    print("Number of     augmented tracks: {0}".format(iface.getAugmentedTrackCount()))

def main(args):
    """Main routine

    \param args Instance of argparse.ArgumentParser
    \return Integer indicating the return code"""

    success = True
    # main actions (mutual exclusive)
    if args.crawl:
        print("Starting to crawl result pages")
        db = openDatabase()
        success = crawlResultpages(db)
    elif args.extend:
        print("Starting to augment tracks")
        db = openDatabase()
        success = augmentTracks(db)
    elif args.statistics:
        print("Printing statistics")
        db = openDatabase()
        success = printStatistics(db)
    elif args.prune:
        print("Starting pruning database")
        db = openDatabase()
        success = pruneDatabase(db)
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
