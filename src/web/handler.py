from lxml import etree
from shared import constants
from shared.db import DatabaseConnection
from shared.interface import TrackInterface
from shared.util import log
from xml.sax.saxutils import escape
import os
import subprocess
import tornado.web

doc_root = os.path.dirname(__file__)

def sanitized(inputStr):
    """Sanitize input for XQuery comparable strings"""

    inputStr = escape(inputStr,
        {'"': ""}
    )
    return inputStr

class MainHandler(tornado.web.RequestHandler):

    def get(self):    
        rawxml = "<?xml version='1.0' encoding='UTF-8'?><response></response>"
        xml = etree.fromstring(rawxml)
        xslt = etree.parse(os.path.join(doc_root,"static/xslt/")+"core.xsl")
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
        searchParam = sanitized(self.get_argument("search", default=""))
        locationParam = sanitized(self.get_argument("location", default=""))
        zipParam = sanitized(self.get_argument("zip", default=""))
        orderCol = self.get_argument("ordercol", default="title")
        orderDir = self.get_argument("orderdir", default="ascending")
        orderType = self.get_argument("ordertype", default="text")


        # TODO: Sanitize input?
        searchString = ""
        if searchParam:
            searchString += ' and contains($x/title/text(), "{0}")'.format(searchParam)
        if zipParam:
            searchString += ' and $x/startPointZip/text() = "{0}"'.format(zipParam)
        if locationParam:
            searchString += ' and contains($x/startPointLocation/text(), "{0}")'.format(locationParam)

        # build query
        queryString = "for $x in track where true()" # use true() here to make the following code less complex
        queryString += searchString
        queryString += " return <track>{$x/title}{$x/fileId}{$x/startPointZip}<pois>{count($x/pois/poi)}</pois></track>"
              
# legacy code (is to slow compared to plain query)        
#        offset = 1
#        limit       
#        queryString2 = """
#let $sortedtrack :=
#    for $x in track where true() {2}
#    return <track>{{$x/title}}{{$x/fileId}}{{$x/startPointZip}}<pois>{{count($x/pois/poi)}}</pois></track>
#    
#for $track in subsequence($sortedtrack, {0}, {1})
#    return $track
#""".format(offset, limit, searchString)
#    
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
        rawXml = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<?xml-stylesheet type=\"text/xsl\" href=\"/static/xslt/core.xsl\"?>
<response>{0}\n<searchresult>\n{1}\n</searchresult>\n</response>""".format(
            searchParamXml, "\n".join(results)
        )
        if False:
            self.set_header("Content-type", "text/xml")
            self.write(rawXml)
        else:
            xml = etree.fromstring(rawXml)
            xslt = etree.parse(os.path.join(doc_root,"static/xslt/")+"core.xsl")
            transform = etree.XSLT(xslt)      
            resulthtml = transform(xml)
            self.write(unicode(resulthtml))
        return

class DetailHandler(tornado.web.RequestHandler):

    def get(self):
        try:
            if True:
                trackId = self.get_argument("id", default="")
                script = "/."+os.path.join(doc_root,"static/")+"helpe.sh"
                subprocess.Popen([script, trackId])   
        except OSError as e:
            log.info('tried to publish kml, failed, but continued request')
        self.post()

    def post(self):
        print('post DetailHandler')
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
        xslt = etree.parse(os.path.join(doc_root,"static/xslt/")+"ajax.xsl")
        transform = etree.XSLT(xslt)      
        resulthtml = transform(xml)
        
        self.write(unicode(resulthtml))
        return

class KmlHandler(tornado.web.RequestHandler):

    def get(self):
        print('get KMLhandler')
        self.post()

    def post(self):
        print('post KMLhandler')
        db = DatabaseConnection(constants.DATABASE_NAME)
        success = db.connect()
        if not success:
            self.write("Database error: {0}".format(db.error))
            return

        # params
        trackId = self.get_argument("id", default="")

        # build query
        queryString = """//track[fileId='{0}']/pois/poi""".format(trackId)
        results = db.query(queryString)

        rawxml = "<?xml version='1.0' encoding='UTF-8'?><response><pois>"+", ".join(results)+"</pois></response>"
        xml = etree.fromstring(rawxml)
        xslt = etree.parse(os.path.join(doc_root,"static/xslt/")+"kml.xsl")
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
