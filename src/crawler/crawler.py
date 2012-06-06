#!/usr/bin/env python

from __future__ import print_function # for print()

# global
import argparse
import urllib2
import os
import sys

# see: http://www.doughellmann.com/PyMOTW/ConfigParser/s
from ConfigParser import SafeConfigParser

# local
from parser import XmlParser
from validator import XmlValidator

# read options file initially
options = SafeConfigParser()
dirname = os.path.dirname(os.path.realpath(__file__))
options.read(os.path.join(dirname, 'config.ini'))

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

def main(args):
    """Main routine

    \param args Instance of argparse.ArgumentParser
    \return Integer indicating the return code"""

    API_BASE_URL = options.get('Common', 'API_BASE_URL')

    # validate
    if not isValidUrl(args.url):
        print("URL is not a valid gpsies.com url")
        print("It needs to be of the form {0}/*".format(API_BASE_URL))
        return 1

    # main routine
    print("URL:         {0}".format(args.url))

    # call correct function based on arguments
    content = readUrl(args.url)

    # main actions (mutual exclusive)
    if args.download is not None:
        print("Saving content to disk")
        saveToFile(content, args.download)
        print("Saved to file: {0}".format(args.download))
    else:
        # default: print XML
        print("Content:")
        print(content)

    # additional actions
    if args.parse:
        # parse + validate content
        tree = parseContent(content)
        schemaFile = sanitizedPath(options.get('Common', 'API_SIMPLE_XML_SCHEMA'))

        print("Trying to validate content...")
        validateContent(tree, schemaFile) # raises if invalid
        print("Ok.")

    return 0 # SUCCESS

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
    parser.add_argument('url', metavar='URL', type=str,
        help='A URL pointing to the gpsies.com API')
    # optional
    parser.add_argument('-p', '--parse', action='store_true',
        help='Parse content and validate')
    parser.add_argument('-d', '--download', metavar='FILE',
        help='Save the XML file')
    args = parser.parse_args()

    rc = main(args)
    sys.exit(rc)
