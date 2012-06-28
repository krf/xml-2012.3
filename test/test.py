#!/usr/bin/env python

from crawlertest import CrawlerTest
from sharedtest import SharedTest
import unittest

def _getTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(CrawlerTest())
    suite.addTest(SharedTest())
    return suite

if __name__ == '__main__':
    # see http://p2p.wrox.com/content/articles/python-test-cases-and-test-suites
    runner = unittest.TextTestRunner()
    testSuite = _getTestSuite()
    runner.run(testSuite)
