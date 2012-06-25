from lxml import etree
from StringIO import StringIO

class XmlParser:

    def __init__(self):
        self.data = None
        self.tree = None

    def parse(self, data):
        """Parse a XML string

        \param data XML string"""

        p = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
        self.tree = etree.parse(StringIO(data), p)
        #self.tree = etree.fromstring(data)

    def dump(self):
        print(etree.tostring(
            self.tree,
            pretty_print=True, method="xml")
        )
