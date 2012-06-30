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
        <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />

	    <title>xml-2012-drei</title>
	    <script type="text/javascript" src="static/js/jquery-1.7.2.min.js"></script>
	    <script type="text/javascript" src="static/js/core.js"></script>
	    <link rel="stylesheet" type="text/css" href="static/bootstrap/css/bootstrap.css"/>
	    <link rel="stylesheet" type="text/css" href="static/core.css"/>
	</head>
</xsl:template>


<!--
	TEMPLATE: searchform
	USE: create htmlsnippet for the searchfields including button
	
	INPUT: -
-->
<xsl:template name="searchform">
    <h1>Neue Suche</h1>
    <form action="/request" method="get" class="well">
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
    <div class="contentcontainer summary">
        <h1>Suchergebnisse <span class="label label-info"><xsl:value-of select="count(track)"/> Treffer</span></h1>
        
        <xsl:choose>
            <xsl:when test="count(track)>0">
                
                <!-- used various times later, so we put it into one var -->
                <xsl:variable name="requestvar">
                    <xsl:value-of select="concat(
                        'search=',
                        //searchparameter/param[@label='search']/@value,
                        '&amp;location=',
                        //searchparameter/param[@label='location']/@value,
                        '&amp;zip=',
                        //searchparameter/param[@label='zip']/@value
                    )"/>
                </xsl:variable>
                
                <div class="summarytable">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>
                                    <a href="/request?{$requestvar}&amp;ordercol=title&amp;orderdir=ascending&amp;ordertype=text"><i class="icon-chevron-up"></i></a> Titel
                                    <a href="/request?{$requestvar}&amp;ordercol=title&amp;orderdir=descending&amp;ordertype=text"><i class="icon-chevron-down"></i></a> 
                                </th>
                                <th>
                                    <a href="/request?{$requestvar}&amp;ordercol=startPointZip&amp;orderdir=ascending&amp;ordertype=text"><i class="icon-chevron-up"></i></a> Ort 
                                    <a href="/request?{$requestvar}&amp;ordercol=startPointZip&amp;orderdir=descending&amp;ordertype=text"><i class="icon-chevron-down"></i></a> 
                                </th>
                                <th>
                                    <a href="/request?{$requestvar}&amp;ordercol=pois&amp;orderdir=ascending&amp;ordertype=number"><i class="icon-chevron-up"></i></a> POIs
                                    <a href="/request?{$requestvar}&amp;ordercol=pois&amp;orderdir=descending&amp;ordertype=number"><i class="icon-chevron-down"></i></a>
                                </th>                        
                            </tr>
                        </thead>
                        <tbody>
                        
                            <!-- can't handle in the xpath-expressions directly into sort, see e.g. [http://stackoverflow.com/questions/2197882/dynamic-sort-in-xslt] -->
                            <xsl:variable name="sortselect">
                              <xsl:value-of select="//searchparameter/param[@label='ordercol']/@value"/>
                            </xsl:variable>                    
                            <xsl:variable name="sortorder">
                              <xsl:value-of select="//searchparameter/param[@label='orderdir']/@value"/>
                            </xsl:variable>
                            <xsl:variable name="sorttype">
                              <xsl:value-of select="//searchparameter/param[@label='ordertype']/@value"/>
                            </xsl:variable>                    
                            <xsl:for-each select="track">
                                <xsl:sort select="*[name() = $sortselect]" order="{$sortorder}" data-type="{$sorttype}"/>
                                <tr>
                                    <td>
                                        <a href="/detail?id={fileId}" target="_blank" class="ajax"><xsl:value-of select="title"/></a>
                                    </td>
                                    <td>
                                        <xsl:value-of select="startPointZip"/>
                                    </td>
                                    <td>
                                        <xsl:value-of select="pois"/>
                                        <!-- <xsl:value-of select="countTrackpoints"/> -->
                                    </td>
                                </tr>
                            </xsl:for-each>
                        </tbody>
                    </table>
                </div>
            </xsl:when>
            <xsl:otherwise>
                <p><span class="label label-warning"><i class="icon-search"></i> Leider gibt es keine passenden Daten zur Suche.</span></p>
            </xsl:otherwise>
        </xsl:choose>
    </div>
    
    <!-- do something here -->
    <div class="contentcontainer detail">
        
    </div>
</xsl:template>


</xsl:stylesheet>