
function initialize () {
  var mapOptions = {zoom: 15};
  var map = new google.maps.Map(
    document.getElementById('main-img'), mapOptions);

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function (position) {
        var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

        map.setCenter(pos);
      }, function (){
        handleNoGeolocation(true);
      });
  } else {
    handleNoGeolocation(false);
  }
}

// google.maps.event.addDomListener(window, 'load', initialize);
