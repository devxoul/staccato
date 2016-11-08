function drawMap() {
  var container = document.getElementById('map');
  var options = {
    center: new daum.maps.LatLng(33.450701, 126.570667),
    level: 3
  };
  var map = new daum.maps.Map(container, options);
  var markerPosition  = new daum.maps.LatLng(33.450701, 126.570667); 
  var marker = new daum.maps.Marker({
      position: markerPosition
  });
  marker.setMap(map);
  // var iwContent = '<div style="padding:5px;">Hello World! <br><a href="http://map.daum.net/link/map/Hello World!,33.450701,126.570667" style="color:blue" target="_blank">큰지도보기</a> <a href="http://map.daum.net/link/to/Hello World!,33.450701,126.570667" style="color:blue" target="_blank">길찾기</a></div>';
  var iwContent = $('#info-window-template').html();
  var iwPosition = new daum.maps.LatLng(33.450701, 126.570667); //인포윈도우 표시 위치입니다
  var infowindow = new daum.maps.InfoWindow({
      position : iwPosition, 
      content : iwContent 
  });
  infowindow.open(map, marker);
}

$(document).ready(function() {
  drawMap();
})
