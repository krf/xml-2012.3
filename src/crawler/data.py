from __future__ import print_function
from lxml import etree
from shared import constants
from shared.db import DatabaseConnection
from shared.interface import TrackInterface
from shared.util import log
import re

def openDatabase():
    # open database
    db = DatabaseConnection(constants.DATABASE_NAME)
    success = db.connect()
    if not success:
        log.error("Database error: {0}".format(db.error))
        raise RuntimeError("Failed to open database")
    return db

def transformTrack(track):
    """Transform the track in our own format

    Transformations
    * Split up startPointAddress -> startPointZip and startPointLocation

    @return True if successful, else False
    """

    trackTree = TrackInterface.toElement(track)
    assert(isinstance(trackTree, etree._Element))

    startPointAddress = trackTree.xpath("startPointAddress")[0]

    m = re.search("([0-9]+) (.+)", startPointAddress.text)
    if not m or len(m.groups()) != 2:
        return False

    zipStr = m.group(1)
    locationStr = m.group(2)

    zipElem = etree.Element("startPointZip")
    zipElem.text = zipStr
    trackTree.append(zipElem)

    locationElem = etree.Element("startPointLocation")
    locationElem.text = locationStr
    trackTree.append(locationElem)

    trackTree.remove(startPointAddress)
    return True
