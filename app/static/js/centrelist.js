document.addEventListener('DOMContentLoaded', function () {
  // Read server-provided coords
  var lat = (window.CENTRELIST && typeof window.CENTRELIST.lat === 'number') ? window.CENTRELIST.lat : -43.5321;
  var lon = (window.CENTRELIST && typeof window.CENTRELIST.lon === 'number') ? window.CENTRELIST.lon : 172.6362;

  var map = L.map('map').setView([lat, lon], 12);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
  }).addTo(map);
});
