var https = require('follow-redirects').https;
const API_KEY = 'AIzaSyA1T_BiFMSg-BVrmkOVGyYBarMtpNeTZgM';
var GoogleMapsAPI = require('googlemaps')

var publicConfig = {
    key: API_KEY,
    stagger_time:       1000, // for elevationPath
    encode_polylines:   false,
    secure:             true, // use https
    proxy:              'http://127.0.0.1:9999' // optional, set a proxy for HTTP requests
  };
var gmAPI = new GoogleMapsAPI(publicConfig);

// geocode API
var geocodeParams = {
    "address":    "121, Curtain Road, EC2A 3AD, London UK",
    "components": "components=country:GB",
    "bounds":     "55,-1|54,1",
    "language":   "en",
    "region":     "uk"
  };
  
gmAPI.geocode(geocodeParams, function(err, result){
    console.log(result);
    if (err) {
        console.log(err);
    }
});

var params = {
    location: '51.507868,-0.087689',
    size: '1200x1600',
    heading: 108.4,
    pitch: 7,
    fov: 40
  };
var result = gmAPI.streetView(params);
https.get(result);
console.log(result);


var placeDetails = function() {
	this.places = [];
}

//Step 1: Get coordinates based on the entered zipcode.

function getCoordinates(zipcode) {
	https.request({
		host: 'maps.googleapis.com',
		path: '/maps/api/geocode/json?address=' + zipcode + '&key=' + API_KEY,
		method: 'GET'},
		CoordinateResponse).end();
}

//Step 2: Find places within the specified radius, based on the coordinates provided by the getCoordinates function.

function placeSearch(latitude, longitude, radius) {
	https.request({
		host: 'maps.googleapis.com',
		path: '/maps/api/place/nearbysearch/json?location=' + latitude + ',' + longitude + '&radius=' + radius + '&type=' + 'restaurant' + '&key=' + API_KEY,
		method: 'GET'},
		PlaceResponse).end();
}

function CoordinateResponse(response) {
	var data = "";
	var sdata = "";
	var latitude = "";
	var longitude = "";

	response.on('data', function(chunk) {
		data += chunk;
	});
	response.on('end', function() {
		sdata = JSON.parse(data);
		latitude = sdata.results[0].geometry.viewport.northeast.lat;
		longitude = sdata.results[0].geometry.viewport.northeast.lng;
		placeSearch(latitude, longitude, 50000);
	});
}

function PlaceResponse(response) {
	var p;
	var data = "";
	var sdata = "";
	var PD = new placeDetails();

	response.on('data', function(chunk) {
		data += chunk;
	});
	response.on('end', function() {
		sdata = JSON.parse(data);
		if (sdata.status === 'OK') {
			console.log('Status: ' + sdata.status);
			console.log('Results: ' + sdata.results.length);
			for (p = 0; p < sdata.results.length; p++) {
				PD.places.push(sdata.results[p]);
			}
			for (r = 0; r < sdata.results.length; r++) {
				console.log('----------------------------------------------');
				console.log(PD.places[r].name);
				console.log('Place ID (for Place Detail search on Google):' + PD.places[r].place_id);
				console.log('Rating: ' + PD.places[r].rating);
				console.log('Vicinity: ' + PD.places[r].vicinity);
			}
		} else {
			console.log(sdata.status);
		}
	});
}

// getCoordinates(94086); //Enter a zip code here