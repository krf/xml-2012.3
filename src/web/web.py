#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys, os

import tornado.ioloop
import tornado.web

from lxml import etree
from pprint import pprint
from shared import constants
from shared.db import DatabaseConnection

class MainHandler(tornado.web.RequestHandler):

    def get(self):
    
        rawxml = "<?xml version='1.0' encoding='ISO-8859-1'?><response></response>"
        xml = etree.fromstring(rawxml)
        xslt = etree.parse(os.path.join(doc_root,"xslt/")+"core.xsl")
        transform = etree.XSLT(xslt)      
        resulthtml = transform(xml)    
        self.write(unicode(resulthtml))
        return

class RequestHandler(tornado.web.RequestHandler):

    def get(self):
        self.post()

    def post(self):
        # FIXME: proper database selection, query string
        db = DatabaseConnection(constants.DATABASE_NAME)
        success = db.connect()
        if not success:
            self.write("Database error: {0}".format(db.error))
            return

        # params
        searchParam = self.get_argument("search", default="")
        locationParam = self.get_argument("location", default="")
        zipParam = self.get_argument("zip", default="")
        orderCol = self.get_argument("ordercol", default="title")
        orderDir = self.get_argument("orderdir", default="ascending")
        orderType = self.get_argument("ordertype", default="text")

        # build query
        queryString = """for $x in //track
            where $x/title/text()[fn:contains(., "{0}")]
            and(not(fn:exists($x/startPointAddress)) or $x/startPointAddress/text()[fn:contains(., "{1}")])
            and(not(fn:exists($x/startPointAddress)) or $x/startPointAddress/text()[fn:contains(., "{2}")])
            return $x""".format(
                searchParam, locationParam, zipParam
            )
        results = db.query(queryString)


        searchparaxml = """
            <searchparameter>
                <param label="search" value="{0}"/>
                <param label="location" value="{1}"/>
                <param label="zip" value="{2}"/>
                <param label="ordercol" value="{3}"/>
                <param label="orderdir" value="{4}"/>
                <param label="ordertype" value="{5}"/>
            </searchparameter>""".format(
            searchParam, locationParam, zipParam, orderCol, orderDir, orderType
        )
        rawxml = "<?xml version='1.0' encoding='UTF-8'?><response>"+searchparaxml+"<searchresult>"+", ".join(results)+"</searchresult></response>"
        xml = etree.fromstring(rawxml)
        xslt = etree.parse(os.path.join(doc_root,"xslt/")+"core.xsl")
        transform = etree.XSLT(xslt)      
        resulthtml = transform(xml)
        
        self.write(unicode(resulthtml))
        return



class DetailHandler(tornado.web.RequestHandler):

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
        trackId = self.get_argument("id", default="")


        # build query
        queryString = """//track[fileId='{0}']""".format(trackId)
        results = db.query(queryString)


        rawxml = "<?xml version='1.0' encoding='UTF-8'?><response><searchresult>"+", ".join(results)+"</searchresult></response>"
        xml = etree.fromstring(rawxml)
        xslt = etree.parse(os.path.join(doc_root,"xslt/")+"ajax.xsl")
        transform = etree.XSLT(xslt)      
        resulthtml = transform(xml)
        
        self.write(unicode(resulthtml))
        return



doc_root = os.path.dirname(__file__)
settings = {
    "static_path": os.path.join(doc_root, "static")
}
pprint(settings)   


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/request", RequestHandler),
    (r"/detail", DetailHandler),
], **settings)

if __name__ == "__main__":
    application.listen(8888)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt. Exit.")
    sys.exit(0)
