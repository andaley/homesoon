// add event listener to info window
google.maps.event.addListener(marker, 'click', calculateDistance)

function calculateDistance() {
  // when user clicks, send server apt ID and calculate distance
  $.get('/calculate-distance', apt_id, function(distance) {
    // return json object containing distance
    // add distance to infoWindow
    $('.window-content').append(distance)
  })
}
