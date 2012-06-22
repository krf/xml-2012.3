from shared import constants
from shared.db import DatabaseConnection
from shared.util import log
import os
import unittest

def _read(path):
    f = open(path, 'r')
    content = f.read()
    return content

class TestBase(unittest.TestCase):

    DATABASE_NAME = "test"

    RESULTPAGE_SAMPLE = _read(os.path.join(constants.RESOURCES_DIR, "resultpage_sample.xml"))
    TRACK_BRIEF_SAMPLE = _read(os.path.join(constants.RESOURCES_DIR, "track_brief_sample.xml"))
    TRACK_DETAILS_SAMPLE = _read(os.path.join(constants.RESOURCES_DIR, "track_details_sample.xml"))

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)

        self.db = None

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.db = self._openDatabase()
        self._clearDatabase()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

        self.db.close()

    def _openDatabase(self):
        db = DatabaseConnection(self.DATABASE_NAME)
        success = db.connect()
        if not success:
            log.error("Database error: {0}".format(db.error))
            raise RuntimeError("Failed to open database")
        return db

    def _clearDatabase(self):#
        self.db.session.execute("DROP DB " + self.DATABASE_NAME)
        self.db.session.execute("CREATE DB " + self.DATABASE_NAME)
        self.db.session.execute("OPEN test")
