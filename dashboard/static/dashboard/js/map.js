var map = L.map('map').setView([48, -72], 6);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    referrerPolicy:'origin-when-cross-origin',
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var stations = JSON.parse(document.getElementById('stations-data').textContent);
var markerEntries = [];

stations.forEach(function (station) {
    var popup = document.createElement('div');
    popup.className = 'station-popup';

    var title = document.createElement('div');
    title.className = 'station-popup-title';
    if (station.station_id) {
        var titleLink = document.createElement('a');
        titleLink.href = station.download_url;
        titleLink.target = '_blank';
        titleLink.rel = 'noopener noreferrer';
        titleLink.textContent = station.name;
        title.appendChild(titleLink);
    } else {
        title.textContent = station.name;
    }
    popup.appendChild(title);

    var table = document.createElement('table');
    var rows = [
        ['Province', station.province],
        ['Climate ID', station.climate_id],
        ['Elevation (m)', station.elevation_m],
        ['Years of record', (station.first_year && station.last_year) ? station.first_year + '–' + station.last_year : null],
        ['Hourly data', (station.hly_first_year && station.hly_last_year) ? station.hly_first_year + '–' + station.hly_last_year : 'No hourly data'],
        ['Daily data', (station.dly_first_year && station.dly_last_year) ? station.dly_first_year + '–' + station.dly_last_year : 'No daily data'],
        ['Monthly data', (station.mly_first_year && station.mly_last_year) ? station.mly_first_year + '–' + station.mly_last_year : 'No monthly data']
    ];
    rows.forEach(function (row) {
        var label = row[0], value = row[1];
        if (value === null || value === undefined || value === '') {
            return;
        }
        var tr = document.createElement('tr');
        var th = document.createElement('th');
        th.textContent = label;
        var td = document.createElement('td');
        td.textContent = value;
        tr.appendChild(th);
        tr.appendChild(td);
        table.appendChild(tr);
    });
    popup.appendChild(table);

    var marker = L.marker([station.latitude, station.longitude]).bindPopup(popup);
    markerEntries.push({ marker: marker, station: station });
});

var markerLayer = L.layerGroup(markerEntries.map(function (entry) { return entry.marker; })).addTo(map);

function stationMatchesFilters(station) {
    var name = document.getElementById('filter-name').value.trim().toLowerCase();
    if (name && station.name.toLowerCase().indexOf(name) === -1) {
        return false;
    }

    var wantHourly = document.getElementById('filter-hourly').checked;
    var wantDaily = document.getElementById('filter-daily').checked;
    var wantMonthly = document.getElementById('filter-monthly').checked;
    if (wantHourly && !(station.hly_first_year && station.hly_last_year)) {
        return false;
    }
    if (wantDaily && !(station.dly_first_year && station.dly_last_year)) {
        return false;
    }
    if (wantMonthly && !(station.mly_first_year && station.mly_last_year)) {
        return false;
    }

    var yearValue = document.getElementById('filter-year').value;
    if (yearValue) {
        var year = parseInt(yearValue, 10);
        if (!(station.first_year && station.last_year && station.first_year <= year && year <= station.last_year)) {
            return false;
        }
    }

    return true;
}

function applyFilters() {
    var visibleCount = 0;
    markerEntries.forEach(function (entry) {
        var matches = stationMatchesFilters(entry.station);
        var onMap = markerLayer.hasLayer(entry.marker);
        if (matches) {
            visibleCount += 1;
            if (!onMap) {
                markerLayer.addLayer(entry.marker);
            }
        } else if (onMap) {
            markerLayer.removeLayer(entry.marker);
        }
    });
    document.getElementById('filter-count').textContent = visibleCount + ' / ' + markerEntries.length + ' stations shown';
}

['filter-name', 'filter-year'].forEach(function (id) {
    document.getElementById(id).addEventListener('input', applyFilters);
});
['filter-hourly', 'filter-daily', 'filter-monthly'].forEach(function (id) {
    document.getElementById(id).addEventListener('change', applyFilters);
});
document.getElementById('filter-reset').addEventListener('click', function () {
    document.getElementById('filter-name').value = '';
    document.getElementById('filter-year').value = '';
    document.getElementById('filter-hourly').checked = false;
    document.getElementById('filter-daily').checked = false;
    document.getElementById('filter-monthly').checked = false;
    applyFilters();
});

applyFilters();
