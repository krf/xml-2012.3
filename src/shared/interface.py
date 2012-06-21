from lxml import etree

from shared.util import log

class TrackInterface:#

    def __init__(self, db):
        self.db = db

    def addTrack(self, track):
        if isinstance(track, str):
            tree = etree.fromstring(track)
        else:
            tree = track

        results = tree.xpath("fileId/text()")
        assert(len(results) == 1)
        fileId = results[0]
        assert(fileId != "")

        log.debug("Adding track with id {0}".format(fileId))
        self.db.session.replace(fileId, etree.tostring(tree))
        return True

    def addTracks(self, tracks):
        for track in tracks:
            self.addTrack(track)

    def getNonAugmentedTracks(self):
        tracks = self.db.query("//track[not(startPointZip)]")
        return tracks

    def getNonAugmentedTracksCount(self):
        result = self.db.query("count(//track[not(startPointZip)])")
        return int(result[0])

    def getAugmentedTracks(self):
        tracks = self.db.query("//track[startPointZip]")
        return tracks

    def getAugmentedTracksCount(self):
        result = self.db.query("count(//track[startPointZip])")
        return int(result[0])
