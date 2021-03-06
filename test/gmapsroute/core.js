$(document).ready(function() {
	loadScript();
});

function loadScript() {
	var script = document.createElement("script");
	script.type = "text/javascript";
	script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyD1SbqmWeSuJL9xRBkGUyaH-tjYSGuBDWk&sensor=false&callback=init";
	document.body.appendChild(script);
}

function init() {
	var mapOptions = {
		zoom : 8,
		mapTypeId : google.maps.MapTypeId.ROADMAP
	}
	map = new google.maps.Map(document.getElementById("mapHolder"), mapOptions);
	loadXmlData(map);
}

function loadXmlData(map) {
	$.get("POI2_example.xml", function(result) {
		console.log("loaded successfully");
		trackDataArray = $("trackData", result).text().split(/\n/);

		mapsTrack = new Array();
		mapBounds = new google.maps.LatLngBounds();

		for (trackPointIndex in trackDataArray) {
			tempTrackSplit = trackDataArray[trackPointIndex].split(/,/);
			tempPoint = new google.maps.LatLng(tempTrackSplit[0], tempTrackSplit[1]);
			mapsTrack.push(tempPoint);
			mapBounds.extend(tempPoint);
		}

		mapsTrackObject = new google.maps.Polyline({
			path : mapsTrack,
			strokeColor : "#0000FF",
			strokeOpacity : 1.0,
			strokeWeight : 2
		})

		mapsTrackObject.setMap(map);
		
		map.fitBounds(mapBounds);

		poiDataArray = $("poi", result);

		for (poiIndex in poiDataArray) {
			currentPoi = poiDataArray[poiIndex];
			console.log("test");
//			new google.maps.Marker({
//				position : new google.maps.LatLng($("lat", currentPoi).text(), $("lon", currentPoi)),
//				map : map,
//				title : $("name", currentPoi).text()
//			});
		}
	});
}