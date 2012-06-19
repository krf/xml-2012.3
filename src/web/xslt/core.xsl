<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="4.0" encoding="utf-8" indent="yes"/>
<xsl:include href="func.xsl"/>


<xsl:template match="response">
    <html>
    <xsl:call-template name="htmlhead"/>

    <body>
        <div class="container-fluid">
            <div class="row-fluid">
                <div class="span3">
                <!--Sidebar content-->
                    <xsl:call-template name="searchform"/>
                </div>
                <div class="span9">
                <!--Body content-->
                    <xsl:apply-templates/>
                </div>
                
            </div>
        </div>
    </body>

    </html>
</xsl:template>

</xsl:stylesheet>
