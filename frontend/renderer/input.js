// import $ from 'jquery';

// on window load
var map;

// on window load
window.onload = function() {
    document.getElementById('navbarDropdownMenuLink').textContent = "potato";

    setMap(43.66074, -79.39661, 'Myhal Centre, Toronto, Ontario, Canada');

    toggleMenuColors('#site-designation-selection');
    toggleMenuColors('#eave-and-ridge-selection');
    toggleMenuColors('#number-height-zone-selection');
    toggleMenuColors('#dominant-opening-selection');
    toggleMenuColors('#single-material-selection');
    toggleMenuColors('#importance-category-selection');


    var siteDesignationSelectionOptions = document.querySelectorAll('#site-designation-selection .btn input');
    for (var i = 0; i < siteDesignationSelectionOptions.length; i++) {
        siteDesignationSelectionOptions[i].addEventListener('change', function() {
            if (this.checked) {
                if (this.id === 'xs_option') {
                    xsCase();
                }
                if (this.id === 'vs30_option') {
                    vs30Case();
                }
            }
        });
    }

    var eaveAndRidgeSelectionOptions = document.querySelectorAll('#eave-and-ridge-selection .btn input');
    for (var i = 0; i < eaveAndRidgeSelectionOptions.length; i++) {
        eaveAndRidgeSelectionOptions[i].addEventListener('change', function() {
            if (this.id === 'eave-and-ridge-yes-option') {
                eaveAndRidgeCase();
            }
            if (this.id === 'eave-and-ridge-no-option') {
                standardDimensionsCase();
            }
        });
    }

    var numberHeightZoneOptions = document.querySelectorAll('#number-height-zone-selection .btn input');
    for (var i = 0; i < numberHeightZoneOptions.length; i++) {
        numberHeightZoneOptions[i].addEventListener('change', function() {
            if (this.id === 'number-height-zone-yes-option') {
                defaultHeightZoneNumberCase();
            }
            if (this.id === 'number-height-zone-no-option') {
                nonDefaultHeightZoneNumberCase();
            }
        });
    }

    var dominantOpeningOptions = document.querySelectorAll('#dominant-opening-selection .btn input');
    for (var i = 0; i < dominantOpeningOptions.length; i++) {
        dominantOpeningOptions[i].addEventListener('change', function() {
            if (this.id === 'dominant-opening-yes-option') {
                dominantOpeningCase();
            }
            else{
                document.getElementById('dominant-opening-container').innerHTML = "";
            }
        });
    }

    var materialOptions = document.querySelectorAll('#single-material-selection .btn input');
    for (var i = 0; i < materialOptions.length; i++) {
        materialOptions[i].addEventListener('change', function() {
            if (this.id === 'single-material-yes-option') {
                singleMaterialCase();
            }

            if (this.id === 'single-material-no-option') {
                multipleMaterialCase();
            }
        });
    }
}

function populateDefaultHeightZoneElevation()
{
    var height = null;

    if (document.getElementById('eave-and-ridge-yes-option').checked)
    {
        var eaveHeight = parseFloat(document.getElementById('eave-height').value);
        var ridgeHeight = parseFloat(document.getElementById('ridge-height').value);
        height = (eaveHeight + ridgeHeight) / 2;
    }

    else if (document.getElementById('eave-and-ridge-no-option').checked)
    {
        height = document.getElementById('height').value;
    }

    if (height) {
        var numHeightZones = Math.ceil(height / 20);
        for (var j = 1; j < numHeightZones + 1; j++) {
            addHeightZoneElevationRow(j * 20);
        }
    }
}

function clearHeightZoneElevationTable()
{
    var table = document.getElementById("height-zone-elevation-table");
    while (table.rows.length !== 1)
    {
        table.deleteRow(-1);
    }
}

function clearMaterialTable()
{
    var table = document.getElementById("material-table");
    while (table.rows.length !== 1)
    {
        table.deleteRow(-1);
    }
}


function heightChange()
{
    if (document.getElementById('number-height-zone-yes-option').checked) {
        clearHeightZoneElevationTable();
        populateDefaultHeightZoneElevation();
    } else if (document.getElementById('number-height-zone-no-option').checked) {
        // pass
    }
    if (document.getElementById('material-table') !== null)
    {
        console.log('line 136');
        heightZoneChange();
    }
}

function materialWeightChange()
{
    if (document.getElementById('single-material-yes-option').checked === true)
    {
        var weight = document.getElementById('material-weight').value;
        clearMaterialTable();
        // iterate through the rows in the height zone elevation table
        var table = document.getElementById("height-zone-elevation-table");
        for (var i = 1; i < table.rows.length; i++)
        {
            addMaterialRow(weight);
        }
    }
}

function heightZoneChange()
{
    console.log('hzc triggered');
    if (document.getElementById('single-material-yes-option').checked === true)
    {
        var weight = document.getElementById('material-weight').value;
        clearMaterialTable();
        // iterate through the rows in the height zone elevation table
        var table = document.getElementById("height-zone-elevation-table");
        for (var i = 1; i < table.rows.length; i++)
        {
            addMaterialRow(weight);
        }
    }

    else if (document.getElementById('single-material-no-option').checked === true)
    {
        clearMaterialTable();
        var table = document.getElementById("height-zone-elevation-table");
        for (var i = 1; i < table.rows.length; i++)
        {
            addMaterialRowEditable();
        }
    }
}

function addHeightZoneElevationRow(elevation) {
    var table = document.getElementById("height-zone-elevation-table");
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    if (table.rows.length === 1)
    {
        cell1.innerHTML = 1;
    }

    else
    {
        cell1.innerHTML = table.rows.length - 1;
    }
    cell2.innerHTML = elevation;
}

function addMaterialRow(weight)
{
    var table = document.getElementById("material-table");
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    if (table.rows.length === 1)
    {
        cell1.innerHTML = 1;
    }

    else
    {
        cell1.innerHTML = table.rows.length - 1;
    }
    cell2.innerHTML = weight;
}

function addHeightZoneElevationRowEditable()
{
    var table = document.getElementById("height-zone-elevation-table");

    console.log(table.rows.length);

    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    if (table.rows.length === 1)
    {
        cell1.innerHTML = 1;
    }

    else
    {
        cell1.innerHTML = table.rows.length - 1;
    }
    cell2.innerHTML = "0";
    cell2.contentEditable = "true";
}

function addMaterialRowEditable()
{
    var table = document.getElementById("material-table");
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    if (table.rows.length === 1)
    {
        cell1.innerHTML = 1;
    }

    else
    {
        cell1.innerHTML = table.rows.length - 1;
    }
    cell2.innerHTML = "0";
    cell2.contentEditable = "true";
}

function removeHeightZoneElevationRow()
{
    var table = document.getElementById("height-zone-elevation-table");
    if (table.rows.length > 1) {
        table.deleteRow(-1);
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


function vs30Case() {
    fetch('subPages/vs30.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('site-designation-sub-selection-container').innerHTML = data;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function xsCase() {
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

function standardDimensionsCase() {
    fetch('subPages/standard_dimensions.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('dimensions-container').innerHTML = data;
            toggleMenuColors('#eave-and-ridge-selection');
            document.getElementById('height').addEventListener('input', heightChange);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function eaveAndRidgeCase() {
    fetch('subPages/eave_and_ridge_dimensions.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('dimensions-container').innerHTML = data;
            toggleMenuColors('#eave-and-ridge-selection');
            document.getElementById('eave-height').addEventListener('input', heightChange);
            document.getElementById('ridge-height').addEventListener('input', heightChange);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function nonDefaultHeightZoneNumberCase() {
    fetch('subPages/non_default_height_zone_number.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('height-zone-elevation-container').innerHTML = data;
            toggleMenuColors('#number-height-zone-selection');
            // document.getElementById('height').addEventListener('input', heightChange);
            // document.addEventListener('input', heightChange);
            // add click event listener for button with id add-height-zone-button
            document.getElementById('add-height-zone-button').addEventListener('click', addHeightZoneElevationRowEditable);
            console.log('ling 342');
            document.getElementById('add-height-zone-button').addEventListener('click', heightZoneChange);
            // add click event listener for button with id remove-height-zone-button
            document.getElementById('remove-height-zone-button').addEventListener('click', removeHeightZoneElevationRow);
            console.log('ling 346');
            document.getElementById('remove-height-zone-button').addEventListener('click', heightZoneChange);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function defaultHeightZoneNumberCase() {
    fetch('subPages/default_height_zone_number.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('height-zone-elevation-container').innerHTML = data;
            toggleMenuColors('#number-height-zone-selection');
            clearHeightZoneElevationTable();
            populateDefaultHeightZoneElevation();
            // document.getElementById('height').addEventListener('input', heightChange);
            // document.addEventListener('input', heightChange);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function dominantOpeningCase() {
    fetch('subPages/dominant_opening.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('dominant-opening-container').innerHTML = data;
            toggleMenuColors('#dominant-opening-selection');
        })
        .catch((error) => {
            console.error('Error:', error);
        });

}


function singleMaterialCase()
{
    fetch('subPages/single_material.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('material-container').innerHTML = data;
            console.log('ling 389');
            heightZoneChange();
            document.getElementById('material-weight').addEventListener('input', materialWeightChange);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function multipleMaterialCase()
{
    fetch('subPages/multiple_material.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('material-container').innerHTML = data;
            console.log('line 400');
            heightZoneChange();
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
    } else {
        if (document.getElementById('xs-A-option').checked) {
            siteDesignation = 'xs';
            seismicValue = 'A';
        } else if (document.getElementById('xs-B-option').checked) {
            siteDesignation = 'xs';
            seismicValue = 'B';
        } else if (document.getElementById('xs-C-option').checked) {
            siteDesignation = 'xs';
            seismicValue = 'C';
        } else if (document.getElementById('xs-D-option').checked) {
            siteDesignation = 'xs';
            seismicValue = 'D';
        } else if (document.getElementById('xs-E-option').checked) {
            siteDesignation = 'xs';
            seismicValue = 'E';
        }
    }

    window.api.invoke('get-token') // Retrieve the token
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
                    if (result.latitude && result.longitude) {
                        setMap(result.latitude, result.longitude, result.address);
                    } else {
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