<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="4.0" encoding="utf-8" indent="yes"/>
<xsl:include href="func.xsl"/>


<xsl:template match="response">
    <h1><xsl:value-of select="//searchresult/track/title"/></h1>
    <h2>(<xsl:value-of select="//searchresult/track/fileId"/>)</h2>
    some more content
    <strong>tweets for number<span id="tsearch"><xsl:value-of select="//searchresult/track/countTrackpoints"/></span></strong>
    <div id="tresults"></div>
</xsl:template>

</xsl:stylesheet>

