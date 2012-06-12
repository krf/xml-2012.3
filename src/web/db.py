from __future__ import print_function

from shared import BaseXClient

class DatabaseConnection:

    def __init__(self, databaseName):
        self._reset()
        self.databaseName = databaseName

        # init

    def _reset(self):
        self.error = None

    def connect(self):
        return self.reconnect()

    def close(self):
        # close session
        if self.session:
            self.session.close()
            self.session = None

    def reconnect(self):
        self._reset()

        self.session = None
        try:
            # create session
            self.session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

        except IOError as e:
            # print exception
            self.error = e
            return False

        return True

    def query(self, queryStr):
        """Return a list of query results"""

        self._reset()

        try:
            session = self.session
            query = session.execute('OPEN {0}'.format(self.databaseName))
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
