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

  console.log('making ajax call now!')
  $.get('/apartments.json', 'hello', function(apts) {
    console.log(apts);
    // TODO: Add markers!
  })

}

google.maps.event.addDomListener(window, 'load', initialize);
