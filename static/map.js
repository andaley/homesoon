
// Define map canvas
var mapCanvas = document.getElementById('main-map');

var mapOptions = {
  center: new google.maps.LatLng(37.7577, -122.4376),
  zoom: 12,
};

// Create the map!
var map = new google.maps.Map(mapCanvas, mapOptions);


function initialize() {
  // Upon page load, recenters map and adds all apartments markers.

  // Define global info window
  var infoWindow = new google.maps.InfoWindow({
    width: 200
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
        title: 'Origin'
      })


    // PUTTING POINTS ON THE MAP, USE DB data
      var apartment, marker, contentString;

      // Make each marker
      var listings = apts['listings']

      for (var key in listings) {
        apartment = listings[key];

            // Define marker for all apts
            marker = new google.maps.Marker({
              position: new google.maps.LatLng(apartment['latitude'], apartment['longitude']),
              map: map,
              animation: google.maps.Animation.DROP,
              title: key
            });

            // CONTENT STRING PER MARKER
            // Define content of infoWindow
            contentString = (
              '<div class="window-content">' +
              '<a href="' + apartment['url'] + '">' + apartment['title'] + '</a>' + '<p>Price: ' + apartment['price'] + '</p>' +
              '<p>Bedrooms: ' + apartment['bedrooms'] + '</p>' +
              // '<img src="' + apartment.img_url + '" height="50px">' +
              '<a href="#" target="_blank" id="' + key + '-dir"><p>Commute time: <span id="' + key + '-time"></span></p></a>' +
              '<p>Commute distance: <span id="' + key + '-distance">' + '</span></p>' +
              '<button class="btn" id="' + key + '-fav">Save to Favorites</button>' +
              '</div>'
            );


            // ADD EVENT LISTENER, PER MARKER
            bindinfoWindow(marker, map, infoWindow, contentString);

    }  // END for loop

  });  // END $.get

} // END INITIALIZE


function bindinfoWindow(marker, map, infoWindow, html) {
  google.maps.event.addListener(marker, 'click', function() {
    // Set infoWindow content and open it when user clicks.
    infoWindow.setContent(html);
    infoWindow.open(map, marker);

    lat = marker.position.G;
    lon = marker.position.K;

    // Given latitude and longitude of marker, retrieve distance and duration from Google Distance Matrix.
    console.log('Calculating distance.')
    $.get('/calculate-distance/' + lat + '/' + lon, function(total_distance) {

      // Updating infoWindow with commute times and distance.
      $('#' + marker.title + '-time').html(total_distance.duration);
      $('#' + marker.title + '-distance').html(total_distance.distance);
      $('#' + marker.title + '-dir').attr('href', total_distance.directions);
    })

    // Add event listener to each 'favorite' button after distance has been calculated.
    $('#' + marker.title + '-fav').on('click', function() {
        console.log('Adding to favorites.');
        console.log($('#' + marker.title + '-distance').val())
        console.log($('#' + marker.title + '-time').val())

        // Add favorite to database & disable button.
        $.get('/add-favorite', {'id': marker.title, 'distance': $('#' + marker.title + '-distance').val()}, function(){
          $('#' + marker.title + '-fav').html('Saved.');
          // disable button
        });

      });

})
}

google.maps.event.addDomListener(window, 'load', initialize);
