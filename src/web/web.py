#!/usr/bin/env python

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(
"""
<html>
<body>
<form action="/request" method="post">
Search: <input type="text" name="search"/><br/>
Location: <input type="text" name="location"/><br/>
ZIP: <input type="text" name="message"/><br/>
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
        # TODO: Write XML here
        self.set_header("Content-Type", "text/plain")
        self.write(
"""\
Search: {0}
Location: {1}
ZIP: {2}"""
.format(
    self.get_argument("search", default=""),
    self.get_argument("location", default=""),
    self.get_argument("message", default=""),
))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/request", RequestHandler)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
