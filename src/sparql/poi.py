from lxml import etree
from SPARQLWrapper import SPARQLWrapper, JSON

from shared.db import DatabaseConnection
from shared import constants

# SPARQL query string, has to be formatted
SPARQL_QUERY = """
               PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
               SELECT ?subject ?label ?lat ?long ?comment WHERE {
               ?subject geo:lat ?lat.
               ?subject geo:long ?long.
               ?subject rdfs:label ?label.
               ?subject rdfs:comment ?comment.
               FILTER(?lat - %f <= %f && %f - ?lat <= %f &&
                      ?long - %f <= %f && %f - ?long <= %f &&
                      lang(?label) = "de"
                      ).
               } LIMIT %d
               """

# For parsing the list of GPS coordinates out
# of a track xml file
XPATH_GPS_DATA = "//trackData/text()"

# Limit of the DBpedia query result
RESULT_LIMIT = 10

# Difference between the GPS coordinates
DISTANCE = 0.05

FIND_ONLY_MINIMUM = True

class POI:

        def __init__(self, label, la, lo, comment):
                self.label = label
                self.latitude = la
                self.longitude = lo
                self.comment = comment

        def __hash__(self):
                return hash(self.label)

# Returns a list of track dom objects with no point of interests
# in order to augment them
def getTrackDocuments():
        database = DatabaseConnection(constants.DATABASE_NAME)
        database.connect()
        documents = database.getAllDocuments()
        database.close()

        verified = []
        for i, doc in enumerate(documents):
                try:
                        parsed = etree.fromstring(doc)
                        if len(parsed.xpath(XPATH_GPS_DATA)) > 0:
                                verified.append(parsed)
                except etree.XMLSyntaxError:
                        print 'Syntax error at document %s' % i

        return [doc for doc in verified if doc.find('.//pois') is None]

# For the SPARQL query the GPS coordinates are parsed and
# returned as a list [latitude, longitude]
# For now the alitude (height) is ignored
def getGpsCoordinates(document):
        resultSet = document.xpath(XPATH_GPS_DATA)[0]
        allCoordinates = [ (float(la), float(lo)) for la, lo, al in (line.split(',') for line in resultSet.split()) ]
        if FIND_ONLY_MINIMUM:
                size = len(allCoordinates)
                return [allCoordinates[0], allCoordinates[size-1]]
        else:
                return allCoordinates

# For retrieving nearby resources a SPARQL query to DBpedia
# has to be constructed and executed
def queryDBpedia(latitude, longitude, distance, limit):

        query = SPARQL_QUERY % (latitude, distance, latitude, distance,
                        longitude, distance, longitude, distance, limit)

        sparql = SPARQLWrapper('http://dbpedia.org/sparql')
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        pois = []
        for result in results['results']['bindings']:
                label = result['label']['value']
                la = result['lat']['value']
                lo = result['long']['value']
                comment = result['comment']['value']
                pois.append(POI(label, la, lo, comment))

        return pois

# Augments the track document with the point of interests
def augmentTrackDocument(document, pois):

        poisNode = etree.Element('pois')
        for poi in pois:
                poiNode = etree.Element('poi')
                nameNode = etree.Element('name')
                latNode = etree.Element('lat')
                lonNode = etree.Element('lon')
                commentNode = etree.Element('comment')
                nameNode.text = poi.label
                latNode.text = poi.latitude
                lonNode.text = poi.longitude
                commentNode.text = poi.comment
                poiNode.append(nameNode)
                poiNode.append(latNode)
                poiNode.append(lonNode)
                poiNode.append(commentNode)
                poisNode.append(poiNode)

        document.append(etree.fromstring(etree.tostring(poisNode, pretty_print = True)))

        return document

# Writes the augmented document back into the database
def writeBack(document):
        database = DatabaseConnection(constants.DATABASE_NAME)
        database.connect()
        fileId = document.find('.//fileId').text
        database.query('replace node //track[fileId = "%s"] with %s' % (fileId, etree.tostring(document)))
        database.close()

def main():
        tracks = getTrackDocuments()
        print 'Found %d documents with no POIs' % len(tracks)
        for i, document in enumerate(tracks):
                pois = []
                coordinates = getGpsCoordinates(document)
                size = len(coordinates)
                for j, (la, lo) in enumerate(coordinates):
                        pois += queryDBpedia(la, lo, DISTANCE, RESULT_LIMIT)
                        print 'Queried %d of %d GPS coordinates' % (j + 1, size)

                writeBack(augmentTrackDocument(document, set(pois)))
                print 'Augmented document %d of %d' % (i + 1, len(tracks))

main()
