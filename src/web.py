#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from pprint import pprint
from web.handler import doc_root, MainHandler, RequestHandler, DetailHandler, \
    StatisticsHandler, KmlHandler
import os
import sys
import tornado.ioloop
import tornado.web

settings = {
    "static_path": os.path.join(doc_root, "static"),
    "debug": True
}
pprint(settings)   

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/request", RequestHandler),
    (r"/detail", DetailHandler),
    (r"/kml", KmlHandler),
    (r"/stats", StatisticsHandler)
], **settings)

if __name__ == "__main__":
    port = 8888
    application.listen(port)

    try:
        print("Starting web server on localhost:{0}".format(port))
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt. Exit.")
    sys.exit(0)
