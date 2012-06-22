from base import TestBase
from crawler import data
from crawler.validator import XmlValidator
from lxml import etree
import unittest

class CrawlerTest(TestBase):

    def setUp(self):
        TestBase.setUp(self)

        self.tree = etree.fromstring(TestBase.TRACK_DETAILS_SAMPLE)

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

    def testValidateTrackBrief(self):
        tree = etree.fromstring(TestBase.TRACK_BRIEF_SAMPLE)
        validator = XmlValidator(XmlValidator.GPSIES_TRACK_BRIEF_SCHEMA)
        validator.validate(tree)

    def testValidateTrackDetails(self):
        tree = etree.fromstring(TestBase.TRACK_DETAILS_SAMPLE)
        validator = XmlValidator(XmlValidator.GPSIES_TRACK_DETAILS_SCHEMA)
        validator.validate(tree)

    def testValidateResultpage(self):
        tree = etree.fromstring(TestBase.RESULTPAGE_SAMPLE)
        validator = XmlValidator(XmlValidator.GPSIES_RESULTPAGE_SCHEMA)
        validator.validate(tree)

if __name__ == '__main__':
    unittest.main()
