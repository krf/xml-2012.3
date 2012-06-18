#!/usr/bin/env python

from __future__ import print_function # for print()

# global
import argparse
import urllib2
import os
import sys
import shutil

from lxml import etree

# see: http://www.doughellmann.com/PyMOTW/ConfigParser/s
from ConfigParser import SafeConfigParser

# local
from parser import XmlParser
from validator import XmlValidator
from shared import constants
from shared.db import DatabaseConnection
from shared.util import log

# read options file initially
options = SafeConfigParser()
dirname = os.path.dirname(os.path.realpath(__file__))

# read defaul config
defaultConfig = os.path.join(dirname, 'config.ini')
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

    f = urllib2.urlopen(url)
    content = f.read()
    return content

def parseContent(content):
    parser = XmlParser()
    parser.parse(content)
    return parser.tree

def validateContent(tree, schemaFile):
    with open(schemaFile, 'r') as f:
        schema = f.read()
        f.close()

        validator = XmlValidator(schema)
        success = validator.validate(tree)

        if not success:
            print("Error: {0}".format(validator.error))

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

def autoRun():
    """Auto-run, crawl from a specific set of pages

    \return True if successful, else False"""

    API_BASE_URL = options.get('Common', 'API_BASE_URL')
    apiKey = getApiKey()

    def getUrl(resultPage):
        url = "{0}/api.do?key={1}&country={2}&limit=100&resultPage={3}".format(
            API_BASE_URL, apiKey, "DE", resultPage
        )
        return url

    # open database
    db = DatabaseConnection(constants.DATABASE_NAME)
    success = db.connect()
    if not success:
        print("Database error: {0}".format(db.error))
        return False

    resultPage = 1
    while True:
        url = getUrl(resultPage)
        log.debug("Parsing URL: {0}".format(url))

        content = readUrl(url)
        tree = parseContent(content)

        tracksSearch = etree.XPath("//track")
        tracks = tracksSearch(tree)
        if len(tracks) == 0:
            break

        # add tracks to database
        db.session.add("tracks", content)
        log.debug("Added {0} tracks to the database".format(len(tracks)))
        resultPage += 1

        # print out number of tracks in db
        queryString = "count(//track)"
        result = db.query(queryString)
        log.debug("Tracks in database: {0}".format(result[0]))

    return True

def main(args):
    """Main routine

    \param args Instance of argparse.ArgumentParser
    \return Integer indicating the return code"""

    API_BASE_URL = options.get('Common', 'API_BASE_URL')

    success = True
    # main actions (mutual exclusive)
    if args.autorun:
        print("Starting auto-run")
        success = autoRun()
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
        schemaFile = sanitizedPath(options.get('Common', 'API_SIMPLE_XML_SCHEMA'))

        print("Trying to validate content...")
        validateContent(tree, schemaFile) # raises if invalid
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
    args = parser.parse_args()

    rc = main(args)
    sys.exit(rc)
