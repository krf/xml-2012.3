from __future__ import print_function
from lxml import etree
from shared.interface import TrackInterface
import re

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
