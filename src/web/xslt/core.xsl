<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="4.0" encoding="utf-8" indent="yes"/>
<xsl:include href="func.xsl"/>


<xsl:template match="/">
    <html>
    <xsl:call-template name="htmlhead"/>

    <body>
        <h1>hello world</h1>
        <!-- do something here -->
        <xsl:call-template name="searchform"/>
    </body>

    </html>
</xsl:template>

</xsl:stylesheet>

