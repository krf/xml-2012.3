from lxml import etree

class XmlParser:

    def __init__(self):
        self.data = None
        self.tree = None

    def parse(self, data):
        """Parse a XML string

        \param data XML string"""

        self.tree = etree.fromstring(data)

    def dump(self):
        print(etree.tostring(
            self.tree,
            pretty_print=True, method="xml")
        )
