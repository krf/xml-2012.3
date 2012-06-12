<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h1>Tracks</h1>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>Trackname</th>
        <th>Length</th>
        <th>Moar</th>
      </tr>
      <xsl:for-each select="result/track">
      <tr>
        <td><xsl:value-of select="title"/></td>
        <td><xsl:value-of select="trackLengthM"/></td>
        <td><a>
            <xsl:attribute name="href">
                <xsl:value-of select="downloadLink"/>
            </xsl:attribute>
            Details
            </a>
        </td>
      </tr>
      </xsl:for-each>
    </table>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>

