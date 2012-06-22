#!/usr/bin/env python

from lxml import etree
from SPARQLWrapper import SPARQLWrapper, JSON

from shared.db import DatabaseConnection
from shared import constants

import logging
import Queue
import thread
import threading
import time
import sys

NUM_THREAD_WORKER = 25

# SPARQL query string, has to be formatted
SPARQL_QUERY = """
               PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
               SELECT ?subject ?label ?lat ?long ?abstract ?wiki ?image WHERE {
               ?subject geo:lat ?lat.
               ?subject geo:long ?long.
               ?subject rdfs:label ?label.
               ?subject dbpedia-owl:abstract ?abstract.
               ?subject foaf:page ?wiki.
               ?subject foaf:depiction ?image.
               FILTER(?lat - %f <= %f && %f - ?lat <= %f &&
                      ?long - %f <= %f && %f - ?long <= %f &&
                      lang(?abstract) = "de" &&
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
DISTANCE = 0.05 # (7.5km)

FIND_ONLY_MINIMUM = True

class POI:

        def __init__(self, label, la, lo, abstract, wiki, image):
                self.label = label
                self.latitude = la
                self.longitude = lo
                self.abstract = abstract
                self.wiki = wiki
                self.image = image

        def __hash__(self):
                return hash(self.label)
        def __eq__(self, other):
                return self.label == other.label

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
                        pass
                        #print 'Syntax error at document %s' % i

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
        
        while True:
                try:
                        results = sparql.query().convert()
                        break
                except Exception as e:
                        pass # swallow and retry

        pois = []
        for result in results['results']['bindings']:
                label = result['label']['value']
                la = result['lat']['value']
                lo = result['long']['value']
                abstract = result['abstract']['value']
                wiki = result['wiki']['value']
                image = result['image']['value']
                pois.append(POI(label, la, lo, abstract, wiki, image))

        return pois

# Augments the track document with the point of interests
def augmentTrackDocument(document, pois):

        poisNode = etree.Element('pois')
        for poi in pois:
                poiNode = etree.Element('poi')
                nameNode = etree.Element('name')
                latNode = etree.Element('lat')
                lonNode = etree.Element('lon')
                abstractNode = etree.Element('abstract')
                wikiNode = etree.Element('wiki')
                imageNode = etree.Element('image')

                nameNode.text = poi.label
                latNode.text = poi.latitude
                lonNode.text = poi.longitude
                abstractNode.text = poi.abstract
                wikiNode.text = poi.wiki
                imageNode.text = poi.image

                poiNode.append(nameNode)
                poiNode.append(latNode)
                poiNode.append(lonNode)
                poiNode.append(abstractNode)
                poiNode.append(wikiNode)
                poiNode.append(imageNode)

                poisNode.append(poiNode)

        document.append(etree.fromstring(etree.tostring(poisNode, pretty_print = True)))

        return document

# Writes the augmented document back into the database
def writeBack(document):
        database = DatabaseConnection(constants.DATABASE_NAME)
        database.connect()
        fileId = document.find('.//fileId').text
        database.session.replace('%s.xml' % fileId, etree.tostring(document))
        database.close()

class SparqlThread(threading.Thread):

        def __init__(self, startTime, size, queue, out):
                threading.Thread.__init__(self)
                self.startTime = startTime
                self.size = size
                self.queue = queue
                self.out = out


        def status(self):

                remaining = self.queue.qsize()
                processed = self.size - remaining
                currentTime = time.time()
                elapsed = currentTime - self.startTime
                estimated = self.size / processed * elapsed

                m, s = divmod(estimated, 60)
                h, m = divmod(m, 60)
                estimatedString = '%dh %dmin' % (h, m)

                approx = 100000 / processed * elapsed 
                m, s = divmod(approx, 60)
                h, m = divmod(m, 60)
                approxString = '%dh %dmin' % (h, m)

                sys.stdout.write('Tracks processed: %d / %d (~ %s) => 100.000 Tracks (~ %s)\r'
                                % (remaining, self.size, estimatedString, approxString))
                sys.stdout.flush()

        def run(self):

                while not self.queue.empty():
                        track = self.queue.get()
                        pois = []
                        for (lat, lon) in getGpsCoordinates(track):
                                pois += queryDBpedia(lat, lon, DISTANCE, RESULT_LIMIT)

                        track = augmentTrackDocument(track, set(pois))
                        self.out.put(track)
                        self.queue.task_done()
                        self.status()

class WriterThread(threading.Thread):

        def __init__(self, queue):
                threading.Thread.__init__(self)
                self.queue = queue

        def run(self):

                while True:

                        if self.queue.empty:
                                time.sleep(3)

                        document = self.queue.get()
                        writeBack(document)
                        self.queue.task_done()


def main():

        logger = logging.getLogger('default')
        logger.setLevel(logging.CRITICAL)

        tracks = getTrackDocuments()

        workQueue = Queue.Queue()
        resultQueue = Queue.Queue()

        for track in tracks:
                workQueue.put(track)

        threads = []
        for i in range(NUM_THREAD_WORKER):
                thread = SparqlThread(time.time(), len(tracks), workQueue, resultQueue)
                thread.setDaemon(True)
                threads.append(thread)
                thread.start()

        writer = WriterThread(resultQueue)
        writer.setDaemon(True)
        writer.start()

        while len(threads) > 0:
                try:
                        threads = [t.join(1000) for t in threads if t is not None and t.isAlive]

                except KeyboardInterrupt:
                        print 'Abort'
                        return


main()
