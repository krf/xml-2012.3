<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" encoding="UTF-8" omit-xml-declaration="no" indent="yes"/>

<xsl:template match="response">
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <name>POI</name>
        <description>Points of interest zur Route dieser ID</description>
    <xsl:for-each select="pois/poi">
        <Placemark>
            <name><xsl:value-of select="name"/></name>
            <description>
                <xsl:value-of select="abstract"/>
<div class="controls">
    <a href="#poi{position()}" class="anchorlink">Zur Liste der Points of Interests</a></div>              
            </description>
            <Point>
                <coordinates><xsl:value-of select="lon"/>,<xsl:value-of select="lat"/>,0</coordinates>
            </Point>
        </Placemark>
    </xsl:for-each>
    </Document>
    </kml>
</xsl:template>

</xsl:stylesheet>