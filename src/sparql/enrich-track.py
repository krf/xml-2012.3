import sys
import libxml2
from SPARQLWrapper import SPARQLWrapper, JSON

XPATH_TRACK_DATA = "//trackData/text()"
DISTANCE = 0.05
LIMIT = 20

# Reads the XML document and returns a list of (latitude, longtiude) tuples
def getGpsCoordinates(doc):
        context = doc.xpathNewContext()
        result = context.xpathEval(XPATH_TRACK_DATA)
        if len(result) > 1:
                print "XPath Query: result set is bigger then expected"
                sys.exit(-1)

        coordinates = []
        for line in str(result[0]).split():
                split = line.split(",")
                coordinates.append((split[0], split[1]))

        return coordinates

# Read the given XML file containing the track data
doc = libxml2.parseFile(sys.argv[1])
latLong = getGpsCoordinates(doc)

enrichment = ""
for i in range(3):

        print "Query " + str(i) + " of " + str(len(latLong))

        # Build SPARQL query
        queryString = """
                        PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
                        SELECT ?subject ?label WHERE {
                        ?subject geo:lat ?lat.
                        ?subject geo:long ?long.
                        ?subject rdfs:label ?label.
                        FILTER(?lat - """ + latLong[i][0] + """ <= """ + str(DISTANCE) + """ && """ + latLong[i][0] + """ - ?lat <= """ + str(DISTANCE) + """ &&
                                ?long - """ + latLong[i][1] + """ <= """ + str(DISTANCE) + """ && """ + latLong[i][1] + """ - ?long <= """ + str(DISTANCE) + """ &&
                                lang(?label) = "en"
                                ).
                        } LIMIT """ + str(LIMIT) + """
                        """

        # Execute SPARQL query
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery(queryString)

        # Construct XML and write the result
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        enrichment += "<locations>\n  <lat>" + latLong[i][0] + "</lat>\n  <long>" + latLong[i][1] + "</long>\n"
        for res in results["results"]["bindings"]:
                enrichment += "  <place>" + res["label"]["value"] + "</place>\n"
        enrichment += "</locations>"

enrichment = "<extra>" + enrichment + "</extra>"
enrichmentDoc = libxml2.parseDoc(enrichment.encode("UTF-8"))
doc.getRootElement().addChild(enrichmentDoc.getRootElement())

f = open("enriched.xml","w")
doc.saveTo(f)
f.close
