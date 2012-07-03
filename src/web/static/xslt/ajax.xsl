<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="utf-8" indent="yes"/>
<xsl:include href="func.xsl"/>


<xsl:template match="response">
    <xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html></xsl:text>    
    <html>
    <xsl:call-template name="htmlhead"/>
    
    <body>
    <script type="text/javascript" src="https://maps.google.com/maps/api/js?sensor=false"></script>
    
    <xsl:for-each select="//searchresult/track[position()=1]"> <!-- remove position()=2 to show all-->
        <xsl:variable name="track" select="."/>
        <span itemscope="" itemtype="http://schema.org/Event">
        <h1><span itemprop="name"><xsl:value-of select="//searchresult/track/title"/></span></h1>
        
        
        <h2 id="tags">Begriffe</h2>
        <!-- various trackproperties in different labels -->     
        <ul class="tags">
            <li><span class="label"><xsl:value-of select="$track/fileId"/></span></li>
            <li><span class="label label-warning"><xsl:value-of select="$track/trackTypes"/></span></li>
            <li><span class="label label-important"><xsl:value-of select="$track/trackCharacters"/></span></li>
            <li><span class="label label-info"><xsl:value-of select="$track/trackProperty"/></span></li>
        </ul>
        <br style="clear: both;"/>
        
        
        <h2 id="verlauf">Verlauf</h2>
        <xsl:variable name="koords" select="$track/trackData"/>
        <!-- googlemaps related -->
        <div id="ajaxstuff">
            <div id="koords" class="invisible"><xsl:value-of select="$koords"/></div>
            <div id="twittercontainer"></div>
            <div id="gmapscontainer"></div>
            <script type="text/javascript">
                initGoogleMaps(<xsl:value-of select="$track/startPointLat"/>, <xsl:value-of select="$track/startPointLon"/>);
                var koords = document.getElementById("koords").innerHTML;
                addRouteToMap(koords);
                addPointsOfInterestToMap('<xsl:value-of select="$track/fileId"/>');
				loadGeneralTweets(<xsl:value-of select="$track/startPointLat"/>, <xsl:value-of select="$track/startPointLon"/>);
            </script>  
            <br style="clear: both"/>
        </div>
       
        
        
        <h2 id="pois">Interessante Punkte</h2>
        <ul class="poilist" id="poilist">
        <xsl:for-each select="$track/pois/poi">
            <li id="poi{position()}" itemscope="" itemtype="http://schema.org/Place">
                <div class="thumbnail"><img itemprop="image" src="{image}" alt="Bild zu {name}" /></div>
                <div class="info">
                    <span class="label label-info"><xsl:value-of select="type"/></span><a itemprop="name"><xsl:value-of select="name"/></a>
                    <p itemprop="description"><xsl:value-of select="abstract"/></p>
                    <p><a itemprop="url" href="{wiki}" target="_blank">Erzähl mir mehr</a></p>
                </div>            
                <span itemprop="geo" itemscope="" itemtype="http://schema.org/GeoCoordinates" class="invisible coords"><xsl:value-of select="concat(lat,' ',lon)"/>
                	<meta itemprop="latitude" content="{lat}" />
                	<meta itemprop="longitude" content="{lon}" />
                </span>
            </li>
        </xsl:for-each> 
        </ul>    
        <br style="clear: both;"/>
       
<!-- old code of old twitter-part, twitter is now embedded with the map and thus, not needed any longer here           
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
-->
	</span>
    </xsl:for-each>
    </body>
    </html>
</xsl:template>

</xsl:stylesheet>

