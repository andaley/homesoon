function autocomplete() {

  // Autocomplete address
  var input = document.getElementById('address');
  console.log(input);
  var options = {
    types: ['geocode']
  };
  var autocomplete = new google.maps.places.Autocomplete(input, options);

}

google.maps.event.addDomListener(window, 'load', autocomplete);
