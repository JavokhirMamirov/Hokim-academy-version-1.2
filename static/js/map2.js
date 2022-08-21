function initMap() {
    let Lat = 40.375056
    let Lng = 69.1585715
    let mapOptions = {
        center: {lat: Lat, lng: Lng},
        zoom: 6
    }

    let map = new google.maps.Map(document.getElementById('simple-map'), mapOptions)

    let markerOptions = {
        position: new google.maps.LatLng(Lat, Lng)
    }

    let marker = new google.maps.Marker(markerOptions)

    marker.setMap(map)
    map.addListener("click", (clickEvent) => {
        marker.setPosition(clickEvent.latLng)
        document.getElementById('lc_lat').value = parseFloat(clickEvent.latLng.lat())
        document.getElementById('lc_lng').value = parseFloat(clickEvent.latLng.lng())
    });
}