<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">




<!--
	TEMPLATE: htmlhead
	USE: create htmlsnippet for the html-head
	
	INPUT: -
-->
<xsl:template name="htmlhead">
	<head>
	    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	    <title>xml-2012-drei</title>
	    <script type="text/javascript" src="http://code.jquery.com/jquery-1.7.2.min.js"></script>
	    <!-- <script type="text/javascript" src="js/core.js"></script> -->
	    <link rel="stylesheet" type="text/css" href="static/bootstrap/css/bootstrap.css"/>
	</head>
</xsl:template>


<!--
	TEMPLATE: searchform
	USE: create htmlsnippet for the searchfields including button
	
	INPUT: -
-->
<xsl:template name="searchform">
    <h1>Neue Suche</h1>
    <form action="/request" method="post" class="well">
        <label for="inSearch">Freitext</label>
        <input id="inSearch" type="text" class="span12" name="search" placeholder="Berge, Brandenburger Tor, ..."/>
        
        <label for="inLocation">Ort</label>
        <input id="inLocation" type="text" class="span12" name="location" placeholder="Berlin, Potsdam, ..."/>
        
        
        <label for="inZIP">Postleitzahl</label>
        <input id="inZIP" type="text" class="span4" name="zip" placeholder="12345"/>
        
        <button type="submit" class="btn">Suche</button>
    </form>

</xsl:template>


<!--
	TEMPLATE: searchresult
	USE: create table of tracks that fit the searchparameter
	
	INPUT: (implizit) searchresult-node of xml with trackrecords
-->
<xsl:template match="searchresult">
    <h1>Suchergebnisse</h1>
    <xsl:choose>
        <xsl:when test="count(track)>0">
            
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th> Titel </th>
                    </tr>
                </thead>
                <tbody>
                    <xsl:for-each select="track">
                        <tr>
                            <td>
                                <xsl:value-of select="title"/>
                            </td>
                        </tr>
                    </xsl:for-each>
                </tbody>
            </table>
        </xsl:when>
        <xsl:otherwise>
            <p><span class="label label-warning"><i class="icon-search"></i> Leider gibt es keine passenden Daten zur Suche.</span></p>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>


</xsl:stylesheet>