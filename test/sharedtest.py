from base import TestBase
from crawler import data
from lxml import etree
from shared.interface import TrackInterface
import unittest

class SharedTest(TestBase):

    def setUp(self):
        TestBase.setUp(self)

    def testAddTrack(self):
        iface = TrackInterface(self.db)
        tracks = iface.getAugmentedTracks()
        self.assertEqual(len(tracks), 0)

        # add non-augmented track
        trackXml = TestBase.TRACK_DETAILS_SAMPLE
        iface.addTrack(trackXml)
        self.assertEqual(iface.getAugmentedTrackCount(), 0)
        self.assertEqual(iface.getNonAugmentedTrackCount(), 1)

        self._clearDatabase()

        # add augmented track
        trackTree = etree.fromstring(trackXml)
        data.transformTrack(trackTree)
        augmentedTrackXml = etree.tostring(trackTree)
        iface.addTrack(augmentedTrackXml)
        self.assertEqual(iface.getAugmentedTrackCount(), 1)
        self.assertEqual(iface.getNonAugmentedTrackCount(), 0)

    def testFindTrack(self):
        iface = TrackInterface(self.db)

        # add some track
        trackXml = TestBase.TRACK_DETAILS_SAMPLE
        iface.addTrack(trackXml)

        # find track again
        fileId = "ninkkhylgvessmmr"
        track = iface.findTrack(fileId)
        self.assertTrue(track)
        trackXml = etree.fromstring(track)
        self.assertEquals(trackXml.xpath("//fileId")[0].text, fileId)

        track = iface.findTrack("foo")
        self.assertFalse(track)

    def testRemoveTrack(self):
        iface = TrackInterface(self.db)

        # add some track
        trackXml = TestBase.TRACK_DETAILS_SAMPLE
        iface.addTrack(trackXml)
        self.assertEqual(iface.getNonAugmentedTrackCount(), 1)

        # delete track
        fileId = TrackInterface.parseFileId(trackXml)
        self.assertTrue(fileId)
        success = iface.removeTrackById(fileId)
        self.assertTrue(success)
        self.assertEqual(iface.getNonAugmentedTrackCount(), 0)

if __name__ == '__main__':
    unittest.main()
