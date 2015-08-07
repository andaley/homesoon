// TODO: add event listener to info window; calculate commute distance with Google Distance Matrix


function initialize() {

  var mapCanvas = document.getElementById('main-map');
  var mapOptions = {
    center: new google.maps.LatLng(37.78, -122.41),
    zoom: 13,
    // mapTypeId: google.maps.mapTypeId.ROADMAP
  };

  var map = new google.maps.Map(mapCanvas, mapOptions);

  // Define global info window
  var infoWindow = new google.maps.InfoWindow({
        width: 200
    })

  // Retrieve apartment objects from server
  $.get('/apartments.json', 'HELLO', function(apts) {
    var apartment, marker, contentString;

    // Iterate through keys in master apts object
    for (var key in apts) {
      apartment = apts[key];

      // Define marker
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(apartment['latitude'], apartment['longitude']),
        map: map,
        title: 'Apartment ID' + apartment['post_id'],
      });

      // Define content of infoWindow
      contentString = (
        '<div class="window-content">'+
        '<a href="' + apartment['url'] + '">' + apartment['title'] + '</a>' + '<p>Price: ' + apartment['price'] + '</p>' +
        '<p>Bedrooms: ' + apartment['bedrooms'] + '</p>' +
        '</div>'
      );

      bindinfoWindow(marker, map, infoWindow, contentString);
    }

  });

  function bindinfoWindow(marker, map, infoWindow, html) {
    google.maps.event.addListener(marker, 'click', function() {
      infoWindow.close();
      infoWindow.setContent(html);
      infoWindow.open(map, marker);
    });
  }

}

google.maps.event.addDomListener(window, 'load', initialize);
