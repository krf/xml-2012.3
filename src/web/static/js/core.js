$(document).ready(function() {
    console.log('start');    
    
	
	
    
    /* load detailinfo of route */
    /* catch every klick on an <a>tag and perform ajaxrequest with href */
    $("div.summary a.ajax").click(function (evt) {
        return;
        evt.preventDefault();
        var target = $(this).attr('href');
        console.log(target);
        
        $.get(target, function(data) {
            $("div.detail").html(data);
            
            /* retrieve some twitterinfo */
            
            $("li.twitterlist").each(function(idx, para) {
               console.log($(this).html());
               var searchstring  = $(this).find("span.tsearch").html();
               
               console.log(idx+" "+para);
               
               var items = []
               var baseurl = "http://search.twitter.com/search.json?callback=?&q="+searchstring+"&lang=de&rpp=5&include_entities=true&result_type=mixed";
                console.log(baseurl);
                $.getJSON(baseurl, function(data) {       
                    if(data.results.length==0) {
                        str = "<li><span class=\"label label-warning\">keine Tweets vorhanden</span></li>"
                    } else {    
                        console.log("return from req"+idx);
                        items[idx] = [];
                        for (i=0; i < data.results.length; i++){
                            row = data.results[i];
                            items[idx].push('<li><span class="label">'+row.from_user+'</span>' +row.text+ '</li>');                
                        }
                        
                        str = items[idx].join('');
                    }          
                    $($("li.twitterlist").get(idx)).find(".tweets").html(str);                    
                });
               
               
            });
           
        });
    }); 
});

function loadGeneralTweets(lat,lon){
	console.log('+info:load general tweets');   
	
	
	
               
               
               
               var baseurl = "http://search.twitter.com/search.json?callback=?&lang=de&rpp=5&include_entities=true&result_type=mixed&geocode="+lat+","+lon+",5km";
               
               // "http://api.twitter.com/1/geo/reverse_geocode.json?callback=?&lang=de&rpp=5&include_entities=true&result_type=mixed&lat="+lat+"&long="+lon;
               // "http://search.twitter.com/search.json?callback=?&q="+searchstring+"&lang=de&rpp=5&include_entities=true&result_type=mixed";
               
           	
               console.log("baseurl: "+baseurl);


                $.getJSON(baseurl, function(data) {    
                	
                	console.log(data.results.length); 
                    if(data.results.length==0) {
                    	console.log("0");  
                        str = "<li><span class=\"label label-warning\">keine Tweets vorhanden</span></li>"
                    } else {
                    	
                        for (i=0; i < data.results.length; i++){
                            
                        	row = data.results[i];
                        	console.log(row.from_user);   
                        	displayTweetInRightBox(row);
                         
                            
                        }
                        
                   
                    }          
                 
                });
               
               
           
}

function displayTweetInRightBox(row){
	$("div#ajaxstuff div#twittercontainer").append('<div class="tweetContainerRight"><span class="label">'+row.from_user+'</span> '+ row.text+'</div>');
}


function initGoogleMaps(_lat, _lon) {
    var latlng = new google.maps.LatLng(_lat, _lon);
    var myOptions = {
        zoom: 13,
        center: latlng,
        scrollwheel: false,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    };
    map = new google.maps.Map(document.getElementById("gmapscontainer"), myOptions);    
}

function addRouteToMap(_routestr) {
    var _route = _routestr.split("\n");
    var routeCoords = new Array(); 
    var mapBounds = new google.maps.LatLngBounds();
    for (var i=0; i<_route.length; i++) {
        point = _route[i];
        llh = point.split(",");
        var tempGcoord = new google.maps.LatLng(llh[0], llh[1]);
        routeCoords.push (tempGcoord);
        mapBounds.extend(tempGcoord);
    }
    
    var flightPath = new google.maps.Polyline({
        path: routeCoords,
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
        
    flightPath.setMap(map);
    map.fitBounds(mapBounds);
    
}

function addPointsOfInterestToMap(id) {
    rand = Math.round(Math.random()*1000);
    url = 'http://www.userpage.fu-berlin.de/andrez/kml/'+id+'.kml'+"?"+rand;
    console.log(url);
    var georssLayer = new google.maps.KmlLayer(url, {preserveViewport: true});
    
    georssLayer.setMap(map);
    
    google.maps.event.addListener(georssLayer, 'click', function(kmlEvent) {
    	var html = kmlEvent.featureData.description;
    	var poi = $(html).find('a').attr('href');
    	var name = kmlEvent.featureData.name;
    	triggerTwittersearch(poi, name);
    });  
}

function triggerTwittersearch(poianchor, title) {
    var geocode = $("#poilist").find(poianchor+" span.coords").html();
    lat = geocode.split(" ")[0];
    lon = geocode.split(" ")[1];
    console.log(geocode);
    $("#twittercontainer").empty();
    
    var baseurl = "http://search.twitter.com/search.json?callback=?&q=&geocode="+geocode+",1km&lang=de&rpp=10&result_type=mixed";
    var baseurl = "http://search.twitter.com/search.json?callback=?&q="+title+"&lang=de&rpp=10&result_type=mixed";
//    var baseurl = "https://api.twitter.com/1/geo/reverse_geocode.json?callback=?&lat="+lat+"&long="+lon;    
        
    console.log(baseurl);
    $.getJSON(baseurl, function(data) {       
        console.log(data);
        for (tweetIndex in data.results) {
        	$.getJSON('https://api.twitter.com/1/statuses/oembed.json?callback=?&id='+data.results[tweetIndex].id_str+'&lang=de&omit_script=false', function(tweetResult) {
        		console.log(tweetResult);
        		$("#twittercontainer").append(tweetResult.html);
        	});
         }
    });   
}
