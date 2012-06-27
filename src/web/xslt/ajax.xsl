<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="4.0" encoding="utf-8" indent="yes"/>
<xsl:include href="func.xsl"/>


<xsl:template match="response">

    <xsl:call-template name="htmlhead"/>
    <script type="text/javascript" src="https://maps.google.com/maps/api/js?sensor=false"></script>

    <xsl:for-each select="//searchresult/track[position()=1]"> <!-- remove position()=2 to show all-->
        <xsl:variable name="track" select="."/>
        
        <h1><xsl:value-of select="//searchresult/track/title"/></h1>
        
        
        <h2><a name="tags">Begriffe</a></h2>
        <!-- various trackproperties in different labels -->     
        <ul class="tags">
            <li><span class="label"><xsl:value-of select="$track/fileId"/></span></li>
            <li><span class="label label-warning"><xsl:value-of select="$track/trackTypes"/></span></li>
            <li><span class="label label-important"><xsl:value-of select="$track/trackCharacters"/></span></li>
            <li><span class="label label-info"><xsl:value-of select="$track/trackProperty"/></span></li>
        </ul>
        <br style="clear: both;"/>
        
        
        <h2><a name="verlauf">Verlauf</a></h2>
        <xsl:variable name="koords" select="$track/trackData"/>
        <!-- googlemaps related -->
        <div id="koords" class="invisible"><xsl:value-of select="$koords"/></div>
        <div id="gmapscontainer"></div>
        <script type="text/javascript">
            initGoogleMaps(<xsl:value-of select="$track/startPointLat"/>, <xsl:value-of select="$track/startPointLon"/>);
            var koords = document.getElementById("koords").innerHTML;
            addRouteToMap(koords);
            // addPointsOfInterestToMap('<xsl:value-of select="$track/fileId"/>');
        </script>         
        
        
        <h2><a name="pois">Interessante Punkte</a></h2>
        <ul class="poilist">
        <xsl:for-each select="$track/pois/poi">
            <li>
                <div class="thumbnail"><img src="{image}"/></div>
                <div class="info">
                    <a name="poi{position()}"><xsl:value-of select="name"/></a>
                    <p><xsl:value-of select="abstract"/></p>
                    <p><a href="{wiki}">Erzähl mir mehr</a></p>
                </div>            
            </li>
        </xsl:for-each> 
        </ul>    
        <br style="clear: both;"/>
            
        <h2><a name="meinungen">Meinungen</a></h2>
        <ul>        
            <li class="twitterlist"><span class="label label-info">Tweets über <span class="tsearch"><xsl:value-of select="$track/title"/></span></span>
                <ul class="tweets">
                
                </ul>
            </li>
            <li class="twitterlist"><span class="label label-info">Tweets über <span class="tsearch"><xsl:value-of select="$track/pois/poi[position()=1]/name"/></span></span>
                <ul class="tweets">
                
                </ul>
            </li>
        </ul>
        <span class="invisible"><xsl:value-of select="//searchresult/track/countTrackpoints"/></span>
    
 
    
    </xsl:for-each>
</xsl:template>

</xsl:stylesheet>

