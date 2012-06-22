#!/usr/bin/env python

from crawler.crawler import openDatabase
from lxml import etree
from shared.interface import TrackInterface
from shared.util import log
import sys
from crawler.data import transformTrack

def main():
    """Convert from old database format"""

    db = openDatabase()
    iface = TrackInterface(db)
    tracks = db.query("//track[startPointAddress]")
    
    iterations = 0
    for trackStr in tracks:
        track = etree.fromstring(trackStr)
        fileId = TrackInterface.parseFileId(track)
        log.debug("Transforming track: {0}".format(fileId))
        transformTrack(track)
        iface.addTrack(track)
        iterations += 1

    log.debug("Finished transforming {0} tracks".format(iterations))
    log.debug("Deleting old 'tracks' path")
    db.delete("tracks")

    return 0

if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
