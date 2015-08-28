console.log('Applying map style.');

var styles = [
  {
    "featureType": "road.highway",
    "elementType": "geometry",
    "stylers": [
      { "hue": "#ff3c00" },
      { "weight": 1.1 },
      { "gamma": 1.57 }
    ]
  },{
    "featureType": "poi.park",
    "elementType": "geometry.fill",
    "stylers": [
      { "hue": "#ff0000" },
      { "color": "#a3be8c" }
    ]
  },{
    "featureType": "water",
    "elementType": "geometry.fill",
    "stylers": [
      { "color": "#5B90BF" },
      { "lightness": 2 },
      { "gamma": 1.91 }
    ]
  },{
    "featureType": "transit.line",
    "elementType": "geometry",
    "stylers": [
      { "weight": 3.5 },
      { "lightness": 8 },
      { "hue": "#00ff99" },
      { "gamma": 2.81 },
      { "color": "#41afa5" },
      { "saturation": -73 }
    ]
  },{
    "featureType": "landscape.man_made",
    "elementType": "geometry",
    "stylers": [
      { "gamma": 0.94 },
      { "lightness": 31 }
    ]
  },{
  }
];

var styledMap = new google.maps.StyledMapType(styles,
    {name: "Styled Map"});
