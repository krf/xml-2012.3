from lxml import etree

class XmlValidator:
    """Validates XML

    \see http://lxml.de/validation.html
    """

    def __init__(self, schema):
        """\param schema String providing the XSLT schema"""

        # validating input
        assert(isinstance(schema, str))

        self.error = None
        self.schema = etree.fromstring(schema)

    def validate(self, tree):
        """Validate a XML tree object

        \note Sets the self.error member if an error occurred

        \return True iff successful, else False
        \param tree An instance of etree.XML()"""

        schema = etree.XMLSchema(self.schema)
        parser = etree.XMLParser(schema = schema)

        try:
            schema.assertValid(tree)
        except etree.DocumentInvalid, e:
            self.error = e
            return False

        return True
