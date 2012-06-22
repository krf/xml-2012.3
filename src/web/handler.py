from lxml import etree
from shared import constants
from shared.db import DatabaseConnection
from shared.interface import TrackInterface
import os
import tornado.web

doc_root = os.path.dirname(__file__)

class MainHandler(tornado.web.RequestHandler):

    def get(self):    
        rawxml = "<?xml version='1.0' encoding='UTF-8'?><response></response>"
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
        # TODO: Sanitize input?
        queryString = "for $x in //track where"
        queryString += ' contains($x/title/text(), "{0}")'.format(searchParam)
        if zipParam:
            queryString += ' and $x/startPointZip/text() = "{0}"'.format(zipParam)
        queryString += ' and contains($x/startPointLocation/text(), "{0}")'.format(locationParam)
        queryString += " return $x"
        print(queryString)
        results = db.query(queryString)

        searchParamXml = """
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
        rawXml = """<?xml version='1.0' encoding='UTF-8'?>
            <response>{0}<searchresult>{1}</searchresult></response>""".format(
            searchParamXml, ", ".join(results)
        )
        xml = etree.fromstring(rawXml)
        xslt = etree.parse(os.path.join(doc_root,"xslt/")+"core.xsl")
        transform = etree.XSLT(xslt)      
        resulthtml = transform(xml)
        
        self.write(unicode(resulthtml))
        return

class DetailHandler(tornado.web.RequestHandler):

    def get(self):
        self.post()

    def post(self):
        db = DatabaseConnection(constants.DATABASE_NAME)
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
        print(rawxml)
        xml = etree.fromstring(rawxml)
        xslt = etree.parse(os.path.join(doc_root,"xslt/")+"ajax.xsl")
        transform = etree.XSLT(xslt)      
        resulthtml = transform(xml)
        
        self.write(unicode(resulthtml))
        return

class StatisticsHandler(tornado.web.RequestHandler):

    def get(self):
        db = DatabaseConnection(constants.DATABASE_NAME)
        success = db.connect()
        if not success:
            self.write("Database error: {0}".format(db.error))
            return

        iface = TrackInterface(db)
        databaseInfo = db.session.execute("info database")

        # TODO: Is there an easier way to write out this HTML?
        self.write("""<html>
<xsl:call-template name="htmlhead"/>

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>xml-2012-drei</title>
    <script type="text/javascript" src="static/js/jquery-1.7.2.min.js"></script>
    <script type="text/javascript" src="static/js/core.js"></script>
    <link rel="stylesheet" type="text/css" href="static/bootstrap/css/bootstrap.css"/>
    <link rel="stylesheet" type="text/css" href="static/core.css"/>
</head>

<body>
<div class="container-fluid">
    <div class="row-fluid">
        <div class="contentcontainer">
        <h1>Statistics</h1>
        Number of tracks: {0}<br/>
        Number of non-augmented tracks: {1}<br/>
        Number of augmented tracks: {2}<br/><br/>

        <h2>Database information</h2>
        <pre>
{3}
        </pre>
        </div>
    </div>
</div>
</body>

</html>""".format(
                  iface.getTrackCount(),
                  iface.getNonAugmentedTrackCount(),
                  iface.getAugmentedTrackCount(),
                  databaseInfo)
        )
