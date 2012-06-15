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
    <form action="/request" method="post">
        Search: <input type="text" name="search"/><br/>
        Location: <input type="text" name="location"/><br/>
        ZIP: <input type="text" name="zip"/><br/>
        <input type="submit" value="Submit" />
    </form>

</xsl:template>


</xsl:stylesheet>