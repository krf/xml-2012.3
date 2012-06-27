from lxml import etree

from shared.util import log

class TrackInterface:#

    def __init__(self, db):
        self.db = db

    @staticmethod
    def toElement(track):
        if isinstance(track, str):
            tree = etree.fromstring(track)
        else:
            tree = track
        return tree

    @staticmethod
    def parseFileId(track):
        tree = TrackInterface.toElement(track)
        results = tree.xpath("fileId/text()")
        if len(results) != 1:
            return None
        fileId = results[0]
        if fileId == "":
            return None

        return fileId

    def addTrack(self, track):
        """Add track

        If a track with the same fileId exists, replace that one
        """

        tree = self.toElement(track)
        fileId = self.parseFileId(tree)
        if not fileId:
            log.warning("Could not add track: File ID null")
            return False

        log.debug("Adding track with id {0}".format(fileId))
        self.db.session.replace(fileId, etree.tostring(tree))
        return True

    def removeTrack(self, track):
        tree = self.toElement(track)
        fileId = self.parseFileId(tree)
        return self.removeTrackById(fileId)

    def removeTrackById(self, fileId):
        if not fileId:
            log.warning("Could not add track: File ID null")
            return False

        log.debug("Removing track with id {0}".format(fileId))
        rc = self.db.session.execute("DELETE {0}".format(fileId))
        print(rc)
        return True

    def addTracks(self, tracks):
        for track in tracks:
            self.addTrack(track)

    def findTrack(self, fileId):
        tracks = self.db.query('//track[fileId="{0}"]'.format(fileId))
        if len(tracks) == 0:
            return None

        if len(tracks) > 1:
            log.warn("TrackInterface.findTrack yielded more than one result!")
        return tracks[0]

    def getTracks(self):
        tracks = self.db.query("//track")
        return tracks

    def getTrackCount(self):
        result = self.db.query("count(//track)")
        return int(result[0])

    def getNonAugmentedTracks(self):
        tracks = self.db.query("//track[not(startPointZip)]")
        return tracks

    def getNonAugmentedTrackCount(self):
        result = self.db.query("count(//track[not(startPointZip)])")
        return int(result[0])

    def getAugmentedTracks(self):
        tracks = self.db.query("//track[startPointZip]")
        return tracks

    def getAugmentedTrackCount(self):
        result = self.db.query("count(//track[startPointZip])")
        return int(result[0])

    def getNonPoiTracks(self):
        tracks = self.db.query("//track[not(pois)]")
        return tracks
    
    def getNonPoiTrackCount(self):
        tracks = self.db.query("count(//track[not(pois)])")
        return tracks

    def getPoiTracks(self):
        tracks = self.db.query("//track[pois]")
        return tracks
    
    def getPoiTrackCount(self):
        tracks = self.db.query("count(//track[pois])")
        return tracks
