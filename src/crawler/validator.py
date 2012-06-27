from lxml import etree
from shared import constants
import os.path

class XmlValidator:
    """Validates XML

    \see http://lxml.de/validation.html
    """

    GPSIES_RESULTPAGE_SCHEMA = "gpsies_resultpage_schema.xml"
    GPSIES_TRACK_BRIEF_SCHEMA = "gpsies_track_brief_schema.xml"
    GPSIES_TRACK_DETAILS_SCHEMA = "gpsies_track_details_schema.xml"
    TRACK_DB_SCHEMA = "track_db_schema.xml"

    def __init__(self, schema):
        """\param schema File providing the XSLT schema (str)"""

        # validating input
        assert(isinstance(schema, str))

        # read schema
        path = os.path.join(constants.DATA_DIR, schema)
        f = open(path, 'r')
        content = f.read()
        self.schema = etree.fromstring(content)

    def validate(self, tree):
        """Validate a XML tree object

        \param tree An instance of etree.XML()"""

        schema = etree.XMLSchema(self.schema)
        try:
            schema.assertValid(tree)
        except etree.DocumentInvalid, e:
            raise RuntimeError(e)
