function mainMap() {
    var location = {lat: 30.601389, lng: -96.314445};
    var map = new google.maps.Map(document.getElementById("map"), {
            zoom: 4,
            center: location
    });
    var marker = new google.maps.Marker({
            position: location,
            map: map
    });
   }