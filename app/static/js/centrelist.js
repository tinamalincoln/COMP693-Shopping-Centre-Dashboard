document.addEventListener('DOMContentLoaded', () => {
  const mapEl = document.getElementById('map');
  const lat = JSON.parse(mapEl.dataset.lat);
  const lon = JSON.parse(mapEl.dataset.lon);

  const map = L.map('map').setView([lat, lon], 12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // Load centres
  const centresDataEl = document.getElementById('centres-data');
  let centres = [];
  try { centres = JSON.parse(centresDataEl.textContent || '[]'); } catch(e) {}

  // Numbered markers
  centres.forEach(c => {
    if (c.lat != null && c.lon != null) {
      const marker = L.marker([c.lat, c.lon]).addTo(map);
      marker.bindPopup(`<strong>${c.number}. ${c.name}</strong><br>${c.location || ''}`);
    }
  });
});
