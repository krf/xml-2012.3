from base import TestBase
from crawler import data
from lxml import etree
import unittest

class CrawlerTest(TestBase):

    def setUp(self):
        TestBase.setUp(self)

        self.tree = etree.fromstring(TestBase.TRACKDETAILS_SAMPLE)

    def testTransform(self):
        tree = self.tree
        tracks = tree.xpath("//track")
        assert(len(tracks) == 1)

        track = tracks[0]
        data.transformTrack(track)

        # TODO: Use Schema to validate this
        assert(len(track.xpath("startPointZip")) == 1)
        assert(len(track.xpath("startPointLocation")) == 1)

if __name__ == '__main__':
    unittest.main()
