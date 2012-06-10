#!/usr/bin/env python

import sys

import tornado.ioloop
import tornado.web

from db import DatabaseConnection

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write(
"""
<html>
<body>
<form action="/request" method="post">
Search: <input type="text" name="search"/><br/>
Location: <input type="text" name="location"/><br/>
ZIP: <input type="text" name="zip"/><br/>
<input type="submit" value="Submit">
</form>
</body>
</html>
"""
        )

class RequestHandler(tornado.web.RequestHandler):

    def get(self):
        self.post()

    def post(self):
        # FIXME: proper database selection, query string
        db = DatabaseConnection("out")
        success = db.connect()
        if not success:
            self.write("Database error: {0}".format(db.error))
            return

        # params
        searchParam = self.get_argument("search", default="")
        locationParam = self.get_argument("location", default="")
        zipParam = self.get_argument("zip", default="")

        # build query
        queryString = """for $x in //track
            where $x/title/text()[fn:contains(., "{0}")]
            and(not(fn:exists($x/startPointAddress)) or $x/startPointAddress/text()[fn:contains(., "{1}")])
            and(not(fn:exists($x/startPointAddress)) or $x/startPointAddress/text()[fn:contains(., "{2}")])
            return $x""".format(
                searchParam, locationParam, zipParam
            )
        results = db.query(queryString)

        self.set_header("Content-Type", "text/plain")
        self.write(
"""\
Search: {0}
Location: {1}
ZIP: {2}

Query string:
{3}

Result:
{4}
"""
.format(
    searchParam, locationParam, zipParam,
    queryString,
    ", ".join(results)
))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/request", RequestHandler)
])

if __name__ == "__main__":
    application.listen(8888)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt. Exit.")
    sys.exit(0)
