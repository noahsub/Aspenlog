// on window load
var map;

// on window load
window.onload = function() {
    document.getElementById('navbarDropdownMenuLink').textContent = "potato";

    setMap(43.66074, -79.39661, 'Myhal Centre, Toronto, Ontario, Canada');

    toggleMenuColors('#site-designation-selection');


    var siteDesignationSelectionOptions = document.querySelectorAll('#site-designation-selection .btn input');
    for (var i = 0; i < siteDesignationSelectionOptions.length; i++) {
        siteDesignationSelectionOptions[i].addEventListener('change', function() {
            if (this.checked) {
                if (this.id === 'xs_option')
                {
                    xsCase();
                }
                if (this.id === 'vs30_option')
                {
                    vs30Case();
                }
            }
        });
    }
}

function setMap(latitude, longitude, address) {
    // If the map already exists, remove it
    if (map) {
        map.remove();
    }

    // Create a new map
    map = L.map('map', {
        attributionControl: false,
    }).setView([latitude, longitude], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    // Add a marker with a popup
    L.marker([latitude, longitude]).addTo(map).bindPopup(address);
}


function vs30Case()
{
    fetch('subPages/vs30.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('site-designation-sub-selection-container').innerHTML = data;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function xsCase()
{
    fetch('subPages/xs.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('site-designation-sub-selection-container').innerHTML = data;
            toggleMenuColors('#xs-type-selection');
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function toggleMenuColors(toggleMenu) {
    document.querySelectorAll(toggleMenu + ' .btn').forEach((button) => {
        button.addEventListener('click', (event) => {
            document.querySelectorAll(toggleMenu + ' .btn').forEach((btn) => {
                btn.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');
        });
    });
}

// location_button click event
document.getElementById('location_button').addEventListener('click', function() {
    // disable button
    document.getElementById('location_button').disabled = true;

    var address = document.getElementById('address').value;

    var siteDesignation = null;
    var seismicValue = null;
    // if vs30 is selected
    if (document.getElementById('vs30_option').checked) {
        siteDesignation = 'xv';
        seismicValue = document.getElementById('vs30').value;
    }

    else{
        if (document.getElementById('xs-A-option').checked) {
            siteDesignation = 'xs';
            seismicValue = 'A';
        }
        else if (document.getElementById('xs-B-option').checked) {
            siteDesignation = 'xs';
            seismicValue = 'B';
        }
        else if (document.getElementById('xs-C-option').checked) {
            siteDesignation = 'xs';
            seismicValue = 'C';
        }
        else if (document.getElementById('xs-D-option').checked) {
            siteDesignation = 'xs';
            seismicValue = 'D';
        }
        else if (document.getElementById('xs-E-option').checked) {
            siteDesignation = 'xs';
            seismicValue = 'E';
        }
    }



    window.api.invoke('get-token')  // Retrieve the token
    .then((token) => {
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("Accept", "application/json");
        myHeaders.append("Authorization", `Bearer ${token}`);

        var raw = JSON.stringify({
            "address": `${address}`,
            "site_designation": `${siteDesignation}`,
            "seismic_value": `${seismicValue}`
        });

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };

        fetch("http://localhost:42613/location", requestOptions)
            .then(response => response.json())
            .then(result => {
                document.getElementById('wind-velocity-pressure').textContent = result.wind_velocity_pressure;
                document.getElementById('ground-snow-load').textContent = result.snow_load;
                document.getElementById('rain-load').textContent = result.rain_load;
                document.getElementById('design-spectral-acceleration-0-2').textContent = result.design_spectral_acceleration_0_2;
                document.getElementById('design-spectral-acceleration-1').textContent = result.design_spectral_acceleration_1;

                // set the map as long as we have a valid latitude and longitude
                if (result.latitude && result.longitude)
                {
                    setMap(result.latitude, result.longitude, result.address);
                }

                else
                {
                    setMap(-70.73964, -8.91217, 'unknown');
                }

                document.getElementById('location_button').disabled = false;

            })
            .catch(error => {
                console.log('error', error);
            })
            .finally(() => {
                document.getElementById('location_button').disabled = false;
            });
    });
});