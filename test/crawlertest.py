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
        self.assertEquals(len(tracks), 1)

        track = tracks[0]
        data.transformTrack(track)

        # TODO: Use Schema to validate this
        self.assertEquals(track.xpath("startPointZip")[0].text,
                          "01683")
        self.assertEquals(track.xpath("startPointLocation")[0].text,
                          "Triebischtal, Tanneberg, Meissen, Sachsen")

if __name__ == '__main__':
    unittest.main()
