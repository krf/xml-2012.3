from shared.db import DatabaseConnection
from shared.util import log
import os
import unittest

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.join(TEST_DIR, '..')
RESOURCES_DIR = os.path.join(ROOT_DIR, 'resources')

def _read(path):
    f = open(path, 'r')
    content = f.read()
    return content

class TestBase(unittest.TestCase):

    DATABASE_NAME = "test"

    TRACKDETAILS_SAMPLE = _read(os.path.join(RESOURCES_DIR, "trackdetails_sample.xml"))

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