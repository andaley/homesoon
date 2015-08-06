
function initialize() {

  var mapCanvas = document.getElementById('main-map');
  var mapOptions = {
    center: new google.maps.LatLng(37.78, -122.41),
    zoom: 12,
    // mapTypeId: google.maps.mapTypeId.ROADMAP
  };

  var map = new google.maps.Map(mapCanvas, mapOptions);
}

google.maps.event.addDomListener(window, 'load', initialize);
