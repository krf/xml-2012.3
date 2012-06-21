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
        trackXml = TestBase.TRACKDETAILS_SAMPLE
        iface.addTrack(trackXml)
        self.assertEqual(iface.getAugmentedTracksCount(), 0)
        self.assertEqual(iface.getNonAugmentedTracksCount(), 1)

        self._clearDatabase()

        # add augmented track
        trackTree = etree.fromstring(trackXml)
        data.transformTrack(trackTree)
        augmentedTrackXml = etree.tostring(trackTree)
        iface.addTrack(augmentedTrackXml)
        self.assertEqual(iface.getAugmentedTracksCount(), 1)
        self.assertEqual(iface.getNonAugmentedTracksCount(), 0)

if __name__ == '__main__':
    unittest.main()
