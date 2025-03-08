let map;

// Function to initialize map
function initMap(lat, lng) {
    map = L.map('map').setView([lat, lng], 15);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Add marker for user location
    L.marker([lat, lng]).addTo(map)
        .bindPopup("You are here!")
        .openPopup();

    // Search for nearby hospitals using Overpass API
    fetchHospitals(lat, lng);
}

// Function to get user location
document.getElementById('recommend-btn').addEventListener('click', () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                initMap(lat, lng);
            },
            () => alert("Location access denied. Please enable location.")
        );
    } else {
        alert("Geolocation is not supported by your browser.");
    }
});

// Function to fetch nearby hospitals using Overpass API
function fetchHospitals(lat, lng) {
    const query = `[out:json];
        (
            node["amenity"="hospital"](around:5000, ${lat}, ${lng});
            way["amenity"="hospital"](around:5000, ${lat}, ${lng});
            relation["amenity"="hospital"](around:5000, ${lat}, ${lng});
        );
        out center;`;

    fetch(`https://overpass-api.de/api/interpreter?data=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            data.elements.forEach(hospital => {
                const hospitalLat = hospital.lat || hospital.center.lat;
                const hospitalLng = hospital.lon || hospital.center.lon;
                const hospitalName = hospital.tags.name || "Unknown Hospital";

                L.marker([hospitalLat, hospitalLng]).addTo(map)
                    .bindPopup(`<b>${hospitalName}</b>`);
            });
        })
        .catch(() => alert("Failed to load hospitals. Try again later."));
}

document.getElementById('drop-area').addEventListener('click', () => {
    document.getElementById('file-input').click();
});

document.getElementById('file-input').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        previewImage(file);
    }
});

document.addEventListener('paste', (event) => {
    const items = (event.clipboardData || event.originalEvent.clipboardData).items;
    for (const item of items) {
        if (item.kind === 'file') {
            const file = item.getAsFile();
            previewImage(file);
            break;
        }
    }
});

function previewImage(file) {
    const img = document.getElementById('preview');
    const reader = new FileReader();
    reader.onload = (event) => {
        img.src = event.target.result;
        img.style.display = 'block';
    };
    reader.readAsDataURL(file);
}
