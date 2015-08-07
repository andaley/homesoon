console.log('hello please')

function initialize() {

  console.log('please work')
  var mapCanvas = document.getElementById('main-map');
  var mapOptions = {
    center: new google.maps.LatLng(37.78, -122.41),
    zoom: 12,
    // mapTypeId: google.maps.mapTypeId.ROADMAP
  };

  var map = new google.maps.Map(mapCanvas, mapOptions);

  // Define global info window
  var infoWindow = new google.maps.InfoWindow({
        width: 100
    })

  console.log('making ajax call now!')

  // Retrieve apartment objects to use as markers
  $.get('/apartments.json', function(apts) {
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
