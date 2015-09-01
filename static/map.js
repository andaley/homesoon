

var mapCanvas = document.getElementById('main-map');
var mapOptions = {
  center: new google.maps.LatLng(37.7577, -122.4376),
  zoom: 12,
  mapTypeControlOptions: {
    mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'map_style']
  }
};

// Create the map!
var map = new google.maps.Map(mapCanvas, mapOptions);
map.mapTypes.set('map_style', styledMap);
map.setMapTypeId('map_style');

var markerList = [];

function initialize() {
  // Upon page load, recenters map and adds all apartments markers.

  // Define global info window
  var infoWindow = new google.maps.InfoWindow({
    width: 300,
  })


  // Retrieve apartment objects from server
  $.get('/apartments.json', function(apts) {

      // Re-center map according to user's origin.
      var center = new google.maps.LatLng(apts['origin_info']['origin_lat'], apts['origin_info']['origin_lon'])
      map.setCenter(center);

      // Set origin marker
      var originMarker = new google.maps.Marker({
        position: new google.maps.LatLng(apts['origin_info']['origin_lat'], apts['origin_info']['origin_lon']),
        map: map,
        animation: google.maps.Animation.DROP,
        icon: 'https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_purple.png',
        title: 'Origin',
        optimized: true, // used for selenium test. Can set to true once test passes.
      })

    // Place markers on map using database data
      var apartment, marker, contentString;

      var listings = apts['listings']

      for (var key in listings) {
        apartment = listings[key];

            // Create marker per apartment object
            marker = new google.maps.Marker({
              position: new google.maps.LatLng(apartment['latitude'], apartment['longitude']),
              map: map,
              animation: google.maps.Animation.DROP,
              title: key
            });

            markerList.push(marker);

            // Set price message to % more or less than the average.
            var percentMoreLess = Math.round(apartment['price'] / apts['avg_rent'] * 100);

            var priceMessage, difference;
            if (percentMoreLess < 100) {
              difference = 100 - percentMoreLess;
              priceMessage = 'style="color:#94AE80">This is ' + difference + '% less than the average price in your search.</p>';
            } else if (percentMoreLess > 100) {
              difference = percentMoreLess - 100;
              priceMessage = 'style="color:#ff3c00">This is ' + difference + '% more than the average price in your search.';
            }

            var imgURL, imgPlaceholder;
            if (apartment['img_url'] !== "") {
              imgPlaceholder = '<img src="' + apartment['img_url'] + '" height="150px">';
            } else {
              imgPlaceholder = '';
            }

            // Define content of infoWindow per marker
            contentString = (
              '<div class="window-content">' +

              '<a href="' + apartment['url'] + '" target="_blank" class="apt-title">' + apartment['title'] + '</a>' +
              '<button class="btn" id="' + key + '-fav"><span class="glyphicon glyphicon-star-empty star"></span></button>' +

              '<p ' + priceMessage + '</p>' +
              '<p>Rent: $' + apartment['price'] + '</p>' +
              '<p>Bedrooms: ' + apartment['bedrooms'] + '</p>' +
              imgPlaceholder +
              '<a href="#" target="_blank" id="' + key + '-dir"><p>Commute time: <span id="' + key + '-time"></span> <span class="glyphicon glyphicon-new-window"></span></p></a>' +
              '<p>Commute distance: <span id="' + key + '-distance">' + '</span></p>' +
              '</div>'
            );


            // Add event listeners per marker
            bindinfoWindow(marker, map, infoWindow, contentString);

    }  // END for loop

    // Recenter map according to number of markers.
    var bounds = new google.maps.LatLngBounds();
    for(i=0;i<markerList.length;i++) {
     bounds.extend(markerList[i].getPosition());
    }

    map.fitBounds(bounds);

  });  // END $.get


} // END initialize


function bindinfoWindow(marker, map, infoWindow, html) {
  google.maps.event.addListener(marker, 'click', function() {
    // Set infoWindow content and open it when user clicks.
    // After distance has been calculated, add event listener to save posting to favorites.

    infoWindow.setContent(html);
    infoWindow.open(map, marker);
    marker.setIcon('https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_grey.png');

    lat = marker.position.G;
    lon = marker.position.K;

    // Given latitude and longitude of marker, retrieve distance and duration from Google Distance Matrix.
    console.log('Calculating distance.');

    $.get('/calculate-distance/' + lat + '/' + lon, function(total_distance) {

      // Updating infoWindow with commute times and distance.
      $('#' + marker.title + '-time').html(total_distance.duration);
      $('#' + marker.title + '-distance').html(total_distance.distance);
      $('#' + marker.title + '-dir').attr('href', total_distance.directions);
    })

    // Add event listener to each 'favorite' button after distance has been calculated.
    $('#' + marker.title + '-fav').on('click', function() {
        console.log('Adding to favorites.');

        // Add favorite to database & disable button.
        // Note: this cannot run until marker event listener has been triggered, since content of infoWindow doesn't exist in the DOM *until* after.
        $.get('/add-favorite', {'id': marker.title, 'commute_time': $('#' + marker.title + '-time').text()}, function(message){
          $('#' + marker.title + '-fav').html(message);
          $('#' + marker.title + '-fav').attr('disabled');
          // disable button
        });

      });

})
}

google.maps.event.addDomListener(window, 'load', initialize);
