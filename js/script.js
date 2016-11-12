function drawMap() {
  var container = document.getElementById('map');

  var latitude = 33.450701;
  var longitude = 126.570667;

  var options = {
    center: new daum.maps.LatLng(latitude, longitude),
    level: 3
  };
  var map = new daum.maps.Map(container, options);
  map.setZoomable(false);

  var markerPosition  = new daum.maps.LatLng(latitude, longitude); 
  var marker = new daum.maps.Marker({
      position: markerPosition
  });
  marker.setMap(map);

  var zoomControl = new daum.maps.ZoomControl();
  map.addControl(zoomControl, daum.maps.ControlPosition.RIGHT);

  var iwContent = $('#info-window-template').html();
  var iwPosition = new daum.maps.LatLng(latitude, longitude);
  var infowindow = new daum.maps.InfoWindow({
      position: iwPosition, 
      content: iwContent 
  });
  infowindow.open(map, marker);
}

$(document).ready(function() {
  drawMap();
})
