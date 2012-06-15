#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys, os

import tornado.ioloop
import tornado.web

from db import DatabaseConnection
from lxml import etree
from pprint import pprint

class MainHandler(tornado.web.RequestHandler):

    def get(self):
    
        rawxml = "<?xml version='1.0' encoding='ISO-8859-1'?><doc></doc>"
        xml = etree.fromstring(rawxml)
        xslt = etree.parse("src/web/xslt/core.xsl")
        transform = etree.XSLT(xslt)      
        resulthtml = transform(xml)    
        self.write(unicode(resulthtml))
        return
        
        self.write(
"""
<html>
<head>
<body>
<img src="favicon.ico"/>
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
        db = DatabaseConnection("GPSies_sample")
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


        rawxml = "<?xml version='1.0' encoding='ISO-8859-1'?><result>"+", ".join(results)+"</result>"
        xml = etree.fromstring(rawxml)
        xslt = etree.parse("src/web/xslt/core.xsl")
        transform = etree.XSLT(xslt)      
        resulthtml = transform(xml)



        #self.set_header("Content-Type", "text/plain")  
        self.write(unicode(resulthtml))
#        self.write(
#            """\
#            Search: {0}
#            Location: {1}
#            ZIP: {2}
#            
#            Query string:
#            {3}
#            
#            Result:
#            {4}
#            """
#            .format(
#                searchParam, locationParam, zipParam,
#                queryString,
#                ", ".join(results)
#            )
#        )

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}
pprint(settings)   


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/request", RequestHandler),
], **settings)

if __name__ == "__main__":
    application.listen(8888)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt. Exit.")
    sys.exit(0)
