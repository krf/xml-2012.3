from lxml import etree
from SPARQLWrapper import SPARQLWrapper, JSON

from web.db import DatabaseConnection

# SPARQL query string, has to be formatted
SPARQL_QUERY = """
               PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
               SELECT ?subject ?label WHERE {
               ?subject geo:lat ?lat.
               ?subject geo:long ?long.
               ?subject rdfs:label ?label.
               FILTER(?lat - %f <= %f && %f - ?lat <= %f &&
                      ?long - %f <= %f && %f - ?long <= %f &&
                      lang(?label) = "en"
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

# Returns a list of track dom objects in order
# to augment them with point of interests
def getTrackDocuments():
        database = DatabaseConnection('database')
        database.connect()
        documents = database.getAllDocuments()
        database.close()
        return [etree.fromstring(doc) for doc in documents]

# For the SPARQL query the GPS coordinates are parsed and
# returned as a list [latitude, longitude]
# For now the alitude (height) is ignored
def getGpsCoordinates(document):
       resultSet = document.xpath(XPATH_GPS_DATA)[0]
       return [ (float(la),float(lo)) for la,lo,al in (line.split(',') for line in resultSet.split()) ]

# For retrieving nearby resources a SPARQL query to DBpedia
# has to be constructed and executed
def queryDBpedia(latitude, longitude, distance, limit):

        query = SPARQL_QUERY % (latitude, distance, latitude, distance,
                        longitude, distance, longitude, distance, limit)


        sparql = SPARQLWrapper('http://dbpedia.org/sparql')
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        return set([result['label']['value'] for result in results['results']['bindings']])

# Augments the track document with the point of interests
def augmentTrackDocument(document, pois):

        augmentation = "<pois>%s</pois>"
        poisXml = ""
        for poi in pois:
                poisXml += "<poi><name>" + poi + "</name></poi>"
        augmentation = augmentation % poisXml

        part = document.find('.//track')
        xml = etree.fromstring(augmentation)
        part.insert(28, xml)

        return document

# Writes the augmented document back into the database
def writeBack(document):
        database = DatabaseConnection('database')
        database.connect()
        database.session.execute('OPEN {0}'.format(database.databaseName))
        print etree.tostring(document)
        database.session.execute('STORE TO troll.xml "%s"' % etree.tostring(document))
        database.close()

def main():
        tracks = getTrackDocuments()
        for document in tracks:
                (la,lo) = getGpsCoordinates(document)[0]
                pois = queryDBpedia(la,lo, DISTANCE, RESULT_LIMIT)
                writeBack(augmentTrackDocument(document, pois))
                

main()
