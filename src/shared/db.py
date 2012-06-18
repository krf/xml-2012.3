from __future__ import print_function

from shared import BaseXClient
from shared.util import log

class DatabaseConnection:
    """Wrapper around BaseXClient
    
    \note API docs: http://docs.basex.org/wiki/Server_Protocol
    
    Use self.session to get the BaseX Session object"""

    def __init__(self, databaseName):
        self._reset()
        self.databaseName = databaseName

    def _reset(self):
        self.error = None

    def connect(self):
        return self.reconnect()

    def close(self):
        # close session
        if self.session:
            self.session.execute('CLOSE')
            self.session.close()
            self.session = None

    def createDatabase(self):
        """Create database"""

        self._reset()

        log.debug("Trying to create the database: " + self.databaseName)

        try:
            self.session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
            self.session.execute('CREATE DB {0}'.format(self.databaseName))
        except IOError as e:
            self.error = e
            return False

    def reconnect(self):
        """Connect to database
        
        If the database doesn't exist, it will be created.
        \return True on success, else False (self.error indicates the error)
        """

        self._reset()

        self.session = None
        try:
            # create session
            self.session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        except IOError as e:
            self.error = e
            return False

        try:
            self.session.execute('OPEN {0}'.format(self.databaseName))
        except IOError as e:
            if "was not found" in str(e):
                success = self.createDatabase()
                if success:
                    self.reconnect()
                else:
                    return

            self.error = e
            return False

        return True

    # For retrieving all the documents present in the database
    def getAllDocuments(self):
        return self.query('collection({0})'.format(self.databaseName))

    def query(self, queryStr):
        """Return a list of query results"""

        self._reset()

        try:
            session = self.session
            query = session.query(queryStr)

            # loop through all results
            results = []
            for result in query.iter():
                results.append(result)

            # close query object
            query.close()

            # return results
            return results

        except IOError as e:
            # print exception
            self.error = e

        return []
