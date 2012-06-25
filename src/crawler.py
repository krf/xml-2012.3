#!/usr/bin/env python

from __future__ import print_function # for print()
from ConfigParser import SafeConfigParser
from crawler import data
from crawler.data import openDatabase
from crawler.parser import XmlParser
from crawler.validator import XmlValidator
from lxml import etree
from shared import constants
from shared.interface import TrackInterface
from shared.util import log
import argparse
import os
import shutil
import sys
import time
import urllib2

# read options file initially
options = SafeConfigParser()

# read defaul config
defaultConfig = os.path.join(constants.DATA_DIR, 'config.ini')
options.read(defaultConfig)

# read per-user config
userConfig = os.path.expanduser('~/.xml2012.3.ini')
if not os.path.isfile(userConfig):
    shutil.copy(defaultConfig, userConfig)
options.read(userConfig)

def getApiKey():
    API_KEY = options.get('Common', 'API_KEY', )
    if not API_KEY:
        raise RuntimeError("API key not set: Set it in {0}".format(userConfig))
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

def validateContent(tree, schema):
    validator = XmlValidator(schema)
    validator.validate(tree) # raises

def saveToFile(content, outputFile):
    with open(outputFile, 'w') as f:
        f.write(content)
        f.close()

def isValidUrl(url):
    API_BASE_URL = options.get('Common', 'API_BASE_URL')

    url = url.replace('http://', '')
    if not url.startswith(API_BASE_URL):
        return False

    return True

def sanitizedPath(path):
    dirname = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dirname, path)

# TODO: Can we avoid adding tracks with duplicate fileIds here?
def autoRun(db):
    """Auto-run, crawl from a specific set of pages

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
        queryString = "count(//track)"
        result = db.query(queryString)
        numberOfTracks = int(result[0]) # update track count
        log.debug("Tracks in database: {0}".format(numberOfTracks))

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

    queryString = "//track[not(startPointAddress)]"
    results = db.query(queryString)

    iterations = 0
    for result in results:
        tree = etree.fromstring(result)
        fileId = tree.xpath("//fileId/text()")[0]

        log.debug("Finding track details for fileId: {0} (iteration {1})".format(fileId, iterations))
        augmentOneTrack(db, fileId)
        iterations += 1

    return True

def getTrackCount(db):
    results = db.query("count(//track)")
    return int(results[0])

def pruneDatabase(db):
    trackCount_old = getTrackCount(db)

    queryString = "delete node //track[not(startPointAddress)]"
    db.query(queryString)

    trackCount_new = getTrackCount(db)
    removedTracksCount = trackCount_old - trackCount_new
    print("Removed tracks count: {0}".format(removedTracksCount))

    return True

def printStatistics(db):
    result = db.query("count(//track[not(startPointAddress)])")
    print("Number of non-augmented tracks: {0}".format(result[0]))

    result = db.query("count(//track/startPointAddress)")
    print("Number of     augmented tracks: {0}".format(result[0]))

def main(args):
    """Main routine

    \param args Instance of argparse.ArgumentParser
    \return Integer indicating the return code"""

    API_BASE_URL = options.get('Common', 'API_BASE_URL')

    success = True
    # main actions (mutual exclusive)
    if args.autorun:
        print("Starting auto-run")
        db = openDatabase()
        success = autoRun(db)
    elif args.extend:
        print("Starting augmenting tracks")
        db = openDatabase()
        success = augmentTracks(db)
    elif args.statistics:
        print("Printing statistics")
        db = openDatabase()
        success = printStatistics(db)
    elif args.clear:
        print("Starting pruning database")
        db = openDatabase()
        success = pruneDatabase(db)
    elif args.parse:
        # validate
        if not isValidUrl(args.parse):
            print("URL is not a valid gpsies.com url")
            print("It needs to be of the form {0}/*".format(API_BASE_URL))
            return 1

        print("URL: {0}".format(args.url))
        content = readUrl(args.url)

        # parse + validate content
        tree = parseContent(content)
        print("Trying to validate content...")
        validateContent(tree, XmlValidator.GPSIES_RESULTPAGE_SCHEMA) # raises if invalid
        success = True
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
    # default args
    #None
    # optional
    parser.add_argument('-p', '--parse', metavar='URL',
        help='Parse content and validate')
    parser.add_argument('-a', '--autorun', action='store_true',
        help='Autorun, crawl from gpsies.com')
    parser.add_argument('-e', '--extend', action='store_true',
        help='Extend existing tracks with track details, crawl from gpsies.com')
    parser.add_argument('-s', '--statistics', action='store_true',
        help='Print database statistics')
    parser.add_argument('-c', '--clear', action='store_true',
        help='Clear database, remove all non-augmented tracks')
    args = parser.parse_args()

    rc = main(args)
    sys.exit(rc)
