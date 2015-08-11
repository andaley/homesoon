// TODO: add event listener to info window; calculate commute distance with Google Distance Matrix


function initialize() {

  // Define map canvas
  var mapCanvas = document.getElementById('main-map');

  // Define global info window
  var infoWindow = new google.maps.InfoWindow({
    width: 200
  })

  // Retrieve apartment objects from server
  $.get('/apartments.json', function(apts) {

    var mapOptions = {
      center: new google.maps.LatLng(apts['origin_info']['origin_lat'], apts['origin_info']['origin_lon']),
      zoom: 13,
      // mapTypeId: google.maps.mapTypeId.ROADMAP
    };

    // Create the map!
    var map = new google.maps.Map(mapCanvas, mapOptions);

    // Set origin marker
    var originMarker = new google.maps.Marker({
      position: new google.maps.LatLng(apts['origin_info']['origin_lat'], apts['origin_info']['origin_lon']),
      map: map,
      animation: google.maps.Animation.DROP,
      icon: 'https://raw.githubusercontent.com/Concept211/Google-Maps-Markers/master/images/marker_purple.png',
      title: 'Origin'
    })

    var apartment, marker, contentString;

    var listings = apts['listings']
      // Iterate through keys in master apts object
    for (var key in listings) {
      apartment = listings[key];

      // TODO: change marker color according to distance
      // Define marker for all apts
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(apartment['latitude'], apartment['longitude']),
        map: map,
        animation: google.maps.Animation.DROP,
        title: key
      });

      // Define content of infoWindow
      contentString = (
        '<div class="window-content">' +
        '<a href="' + apartment['url'] + '">' + apartment['title'] + '</a>' + '<p>Price: ' + apartment['price'] + '</p>' +
        '<p>Bedrooms: ' + apartment['bedrooms'] + '</p>' +
        '<img src="' + apartment['img_url'] + '" height="50px">' + '<span id="distance">' + '</span>' +
        '</div>'
      );

      bindinfoWindow(marker, map, infoWindow, contentString);
    }


  });

}


function bindinfoWindow(marker, map, infoWindow, html) {
  google.maps.event.addListener(marker, 'click', function() {
    infoWindow.close();
    infoWindow.setContent(html);
    infoWindow.open(map, marker);

    lat = marker.position.G
    lon = marker.position.K

    console.log('Making AJAX request now')
    $.get('/calculate-distance/' + lat + '/' + lon, function(total_distance) {
      html = html + '<p>Commute time: ' + total_distance.duration + '</p>' + '<p>Miles from origin:' + total_distance.distance + '</p>';
      infoWindow.setContent(html);
    });

  });
}

google.maps.event.addDomListener(window, 'load', initialize);
