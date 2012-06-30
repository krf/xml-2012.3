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


function initGoogleMaps(_lat, _lon) {
    var latlng = new google.maps.LatLng(_lat, _lon);
    var myOptions = {
        zoom: 13,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    };
    map = new google.maps.Map(document.getElementById("gmapscontainer"), myOptions);    
}

function addRouteToMap(_routestr) {
    var _route = _routestr.split("\n");
    var routeCoords = new Array(); 
    for (var i=0; i<_route.length; i++) {
        point = _route[i];
        llh = point.split(",");
        routeCoords.push (new google.maps.LatLng(llh[0], llh[1]));
    }
    
    var flightPath = new google.maps.Polyline({
        path: routeCoords,
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
        
    flightPath.setMap(map);    
    
}

function addPointsOfInterestToMap(id) {
    url = 'http://www.userpage.fu-berlin.de/andrez/kml/'+id+'.kml';
    console.log(url);
    var georssLayer = new google.maps.KmlLayer(url);
    georssLayer.setMap(map);
}