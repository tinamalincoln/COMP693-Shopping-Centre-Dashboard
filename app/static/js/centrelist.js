// app/static/js/centrelist.js
document.addEventListener('DOMContentLoaded', function () {
  const mapEl = document.getElementById('map');
  const lat = parseFloat(mapEl.dataset.lat);
  const lon = parseFloat(mapEl.dataset.lon);

  const map = L.map('map').setView([lat, lon], 12);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
  }).addTo(map);
});

