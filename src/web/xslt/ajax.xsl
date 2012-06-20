<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="4.0" encoding="utf-8" indent="yes"/>
<xsl:include href="func.xsl"/>


<xsl:template match="response">
    <xsl:call-template name="htmlhead"/>

    <xsl:variable name="track" select="//searchresult/track[position()=1]"/>
    <h1><xsl:value-of select="//searchresult/track/title"/></h1>
    <ul>
        <li><span class="label">Trackid</span><xsl:value-of select="$track/fileId"/></li>
        <li><span class="label label-info">Länge</span><xsl:value-of select="$track/trackLengthM"/></li> 
        <li><span class="label label-important">Typ</span>
            <xsl:for-each select="$track/trackTypes"><xsl:value-of select="trackType"/> </xsl:for-each>
        </li>
        
        <li class="twitterlist"><span class="label label-info">Tweets über <span class="tsearch"><xsl:value-of select="count($track/pois/poi)"/></span></span>
            <ul class="tweets">
            
            </ul>
        </li>

        <li class="twitterlist"><span class="label label-info">Tweets über <span class="tsearch"><xsl:value-of select="$track/pois/poi[position()=4]/name"/></span></span>
            <ul class="tweets">
            
            </ul>
        </li>
    </ul>
    <span class="invisible"><xsl:value-of select="//searchresult/track/countTrackpoints"/></span>
</xsl:template>

</xsl:stylesheet>

