////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// input.js
// This file contains the scripts for the input page.
//
// Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code
// By using this code, you agree to abide by the terms and conditions in those files.
//
// Author: Noah Subedar [https://github.com/noahsub]
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// GLOBALS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// the map used for location of climatic and seismic data
let MAP;

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// HELPER FUNCTIONS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function ascending(list) {
  for (let i = 1; i < list.length; i++) {
    if (list[i] < list[i - 1]) {
      return false;
    }
  }
  return true;
}

/**
 * Get the float value of an input element with the given id
 * @param id
 * @returns {number|null}
 */
function getFloatValue(id) {
  let element = document.getElementById(id);
  return element ? parseFloat(element.value) : null;
}

/**
 * Get the int value of an input element with the given id
 * @param id
 * @returns {number|null}
 */
function getIntValue(id) {
  let element = document.getElementById(id);
  return element ? parseInt(element.value) : null;
}

/**
 * Get the string value of an input element with the given id
 * @param id
 * @returns {*|null}
 */
function getStrValue(id) {
  let element = document.getElementById(id);
  return element ? element.value : null;
}

/**
 * Set the color of toggle menu buttons when clicked
 * @param toggleMenu
 */
function toggleMenuColors(toggleMenu) {
  document.querySelectorAll(toggleMenu + " .btn").forEach((button) => {
    button.addEventListener("click", (event) => {
      document.querySelectorAll(toggleMenu + " .btn").forEach((btn) => {
        btn.classList.remove("selected");
      });
      event.currentTarget.classList.add("selected");
    });
  });
}

/**
 * Get the seismic parameters
 * @returns {{siteDesignation: string, seismicValue: string}}
 */
function getSeismicParameters() {
  let siteDesignation = null;
  let seismicValue = null;
  // if vs30 is selected
  if (document.getElementById("vs30_option").checked) {
    siteDesignation = "xv";
    seismicValue = document.getElementById("vs30").value;
  } else if (document.getElementById("xs_option").checked) {
    if (document.getElementById("xs-A-option").checked) {
      siteDesignation = "xs";
      seismicValue = "A";
    } else if (document.getElementById("xs-B-option").checked) {
      siteDesignation = "xs";
      seismicValue = "B";
    } else if (document.getElementById("xs-C-option").checked) {
      siteDesignation = "xs";
      seismicValue = "C";
    } else if (document.getElementById("xs-D-option").checked) {
      siteDesignation = "xs";
      seismicValue = "D";
    } else if (document.getElementById("xs-E-option").checked) {
      siteDesignation = "xs";
      seismicValue = "E";
    }
  }
  return {
    siteDesignation,
    seismicValue,
  };
}

/**
 * Set the simple model image. If the image is not found, attempt to fetch the image again.
 * @param connectionAddress
 * @param id
 * @param img
 * @param attempt
 */
function setSimpleModelImage(connectionAddress, id, img, attempt = 10) {
  fetch(`${connectionAddress}/get_simple_model?id=${id}`)
    .then((response) => {
      if (response.status === 200) {
        img.src = `${connectionAddress}/get_simple_model?id=${id}`;
        img.style.maxWidth = "50%";
        img.style.backgroundColor = "#efe8de";
        let images = document
          .getElementById("building-view-container")
          .getElementsByTagName("img");
        while (images.length > 0) {
          images[0].parentNode.removeChild(images[0]);
        }
        document.getElementById("building-view-container").appendChild(img);
      } else {
        if (attempt > 0) {
          return setSimpleModelImage(connectionAddress, id, img, attempt - 1);
        } else {
          throw new Error("Simple Model Image Not Found");
        }
      }
    })
    .catch((error) => console.error(error));
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// TOGGLE CASE FUNCTIONS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Fetch the vs30 sub page and set the innerHTML of the site-designation-sub-selection-container to the data
 */
function vs30Case() {
  fetch("subPages/vs30.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById(
        "site-designation-sub-selection-container",
      ).innerHTML = data;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

/**
 * Fetch the xs sub page and set the innerHTML of the site-designation-sub-selection-container to the data
 */
function xsCase() {
  fetch("subPages/xs.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById(
        "site-designation-sub-selection-container",
      ).innerHTML = data;
      toggleMenuColors("#xs-type-selection");
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

/**
 * Fetch the standard dimensions sub page and set the innerHTML of the dimensions-container to the data
 */
function standardDimensionsCase() {
  fetch("subPages/standard_dimensions.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("dimensions-container").innerHTML = data;
      toggleMenuColors("#eave-and-ridge-selection");
      document.getElementById("height").addEventListener("input", heightChange);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

/**
 * Fetch the eave and ridge dimensions sub page and set the innerHTML of the dimensions-container to the data
 */
function eaveAndRidgeCase() {
  fetch("subPages/eave_and_ridge_dimensions.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("dimensions-container").innerHTML = data;
      toggleMenuColors("#eave-and-ridge-selection");
      document
        .getElementById("eave-height")
        .addEventListener("input", heightChange);
      document
        .getElementById("ridge-height")
        .addEventListener("input", heightChange);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

/**
 * Fetch the non default height zone number sub page and set the innerHTML of the height-zone-elevation-container
 * to the data
 */
function nonDefaultHeightZoneNumberCase() {
  fetch("subPages/non_default_height_zone_number.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("height-zone-elevation-container").innerHTML =
        data;
      toggleMenuColors("#number-height-zone-selection");
      // add click event listener for button with id add-height-zone-button
      document
        .getElementById("add-height-zone-button")
        .addEventListener("click", addHeightZoneElevationRowEditable);
      document
        .getElementById("add-height-zone-button")
        .addEventListener("click", heightZoneChange);
      // add click event listener for button with id remove-height-zone-button
      document
        .getElementById("remove-height-zone-button")
        .addEventListener("click", removeHeightZoneElevationRow);
      document
        .getElementById("remove-height-zone-button")
        .addEventListener("click", heightZoneChange);
      heightZoneChange();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

/**
 * Fetch the default height zone number sub page and set the innerHTML of the height-zone-elevation-container
 * to the data
 */
function defaultHeightZoneNumberCase() {
  fetch("subPages/default_height_zone_number.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("height-zone-elevation-container").innerHTML =
        data;
      toggleMenuColors("#number-height-zone-selection");
      clearHeightZoneElevationTable();
      populateDefaultHeightZoneElevation();
      heightZoneChange();
      document
        .getElementById("material-weight")
        .addEventListener("input", materialWeightChange);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

/**
 * Fetch the dominant opening sub page and set the innerHTML of the dominant-opening-container to the data
 */
function dominantOpeningCase() {
  fetch("subPages/dominant_opening.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("dominant-opening-container").innerHTML = data;
      toggleMenuColors("#dominant-opening-selection");
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

/**
 * Fetch the single material sub page and set the innerHTML of the material-container to the data
 */
function singleMaterialCase() {
  fetch("subPages/single_material.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("material-container").innerHTML = data;
      heightZoneChange();
      document
        .getElementById("material-weight")
        .addEventListener("input", materialWeightChange);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

/**
 * Fetch the multiple material sub page and set the innerHTML of the material-container to the data
 */
function multipleMaterialCase() {
  fetch("subPages/multiple_material.html")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("material-container").innerHTML = data;
      heightZoneChange();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// TOGGLE FUNCTIONS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Handles site designation selection options
 */
function siteDesignationSelection() {
  let siteDesignationSelectionOptions = document.querySelectorAll(
    "#site-designation-selection .btn input",
  );
  for (let i = 0; i < siteDesignationSelectionOptions.length; i++) {
    siteDesignationSelectionOptions[i].addEventListener("change", function () {
      if (this.checked) {
        if (this.id === "xs_option") {
          xsCase();
        }
        if (this.id === "vs30_option") {
          vs30Case();
        }
      }
    });
  }
}

/**
 * Handles eave and ridge selection options
 */
function eaveAndRidgeSelection() {
  let eaveAndRidgeSelectionOptions = document.querySelectorAll(
    "#eave-and-ridge-selection .btn input",
  );
  for (let i = 0; i < eaveAndRidgeSelectionOptions.length; i++) {
    eaveAndRidgeSelectionOptions[i].addEventListener("change", function () {
      if (this.id === "eave-and-ridge-yes-option") {
        eaveAndRidgeCase();
      }
      if (this.id === "eave-and-ridge-no-option") {
        standardDimensionsCase();
      }
    });
  }
}

/**
 * Handles number of height zone selection options
 */
function numberHeightZoneSelection() {
  let numberHeightZoneOptions = document.querySelectorAll(
    "#number-height-zone-selection .btn input",
  );
  for (let i = 0; i < numberHeightZoneOptions.length; i++) {
    numberHeightZoneOptions[i].addEventListener("change", function () {
      if (this.id === "number-height-zone-yes-option") {
        defaultHeightZoneNumberCase();
      }
      if (this.id === "number-height-zone-no-option") {
        nonDefaultHeightZoneNumberCase();
      }
    });
  }
}

/**
 * Handles dominant opening selection options
 */
function dominantOpeningSelection() {
  let dominantOpeningOptions = document.querySelectorAll(
    "#dominant-opening-selection .btn input",
  );
  for (let i = 0; i < dominantOpeningOptions.length; i++) {
    dominantOpeningOptions[i].addEventListener("change", function () {
      if (this.id === "dominant-opening-yes-option") {
        dominantOpeningCase();
      } else {
        document.getElementById("dominant-opening-container").innerHTML = "";
      }
    });
  }
}

/**
 * Handles single material selection options
 */
function materialSelection() {
  let materialSelectionOptions = document.querySelectorAll(
    "#single-material-selection .btn input",
  );
  for (let i = 0; i < materialSelectionOptions.length; i++) {
    materialSelectionOptions[i].addEventListener("change", function () {
      if (this.id === "single-material-yes-option") {
        singleMaterialCase();
      }

      if (this.id === "single-material-no-option") {
        multipleMaterialCase();
      }
    });
  }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// TABLE FUNCTIONS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Clear the height zone elevation table
 */
function clearHeightZoneElevationTable() {
  let table = document.getElementById("height-zone-elevation-table");
  while (table.rows.length !== 1) {
    table.deleteRow(-1);
  }
}

/**
 * Clear the material table
 */
function clearMaterialTable() {
  let table = document.getElementById("material-table");
  while (table.rows.length !== 1) {
    table.deleteRow(-1);
  }
}

/**
 * Add a row to the height zone elevation table
 * @param elevation
 */
function addHeightZoneElevationRow(elevation) {
  let table = document.getElementById("height-zone-elevation-table");
  let row = table.insertRow(-1);
  let cell1 = row.insertCell(0);
  let cell2 = row.insertCell(1);
  if (table.rows.length === 1) {
    cell1.innerHTML = (1).toString();
  } else {
    cell1.innerHTML = (table.rows.length - 1).toString();
  }
  cell2.innerHTML = elevation;
}

/**
 * Add a row to the material table
 * @param weight
 */
function addMaterialRow(weight) {
  let table = document.getElementById("material-table");
  let row = table.insertRow(-1);
  let cell1 = row.insertCell(0);
  let cell2 = row.insertCell(1);
  if (table.rows.length === 1) {
    cell1.innerHTML = (1).toString();
  } else {
    cell1.innerHTML = (table.rows.length - 1).toString();
  }
  cell2.innerHTML = weight;
}

/**
 * Add a row to the height zone elevation table that is editable
 */
function addHeightZoneElevationRowEditable() {
  let table = document.getElementById("height-zone-elevation-table");
  let row = table.insertRow(-1);
  let cell1 = row.insertCell(0);
  let cell2 = row.insertCell(1);
  if (table.rows.length === 1) {
    cell1.innerHTML = 1;
  } else {
    cell1.innerHTML = table.rows.length - 1;
  }
  cell2.innerHTML = "0";
  cell2.contentEditable = "true";
}

/**
 * Add a row to the material table
 */
function addMaterialRowEditable() {
  let table = document.getElementById("material-table");
  let row = table.insertRow(-1);
  let cell1 = row.insertCell(0);
  let cell2 = row.insertCell(1);
  if (table.rows.length === 1) {
    cell1.innerHTML = 1;
  } else {
    cell1.innerHTML = table.rows.length - 1;
  }
  cell2.innerHTML = "0";
  cell2.contentEditable = "true";
}

/**
 * Remove the last row from the height zone elevation table
 */
function removeHeightZoneElevationRow() {
  let table = document.getElementById("height-zone-elevation-table");
  if (table.rows.length > 1) {
    table.deleteRow(-1);
  }
}

function getHeight() {
  let height = null;

  if (document.getElementById("eave-and-ridge-yes-option").checked) {
    let eaveHeight = parseFloat(document.getElementById("eave-height").value);
    let ridgeHeight = parseFloat(document.getElementById("ridge-height").value);
    height = (eaveHeight + ridgeHeight) / 2;
  } else if (document.getElementById("eave-and-ridge-no-option").checked) {
    height = document.getElementById("height").value;
  }

  return height;
}

function getTallestElevation() {
  // get the value of the last elevation cell in the height zone table;
  let table = document.getElementById("height-zone-elevation-table");
  if (table.rows.length === 1) {
    return 0;
  }
  let lastRow = table.rows[table.rows.length - 1];
  let lastCell = lastRow.cells[1];
  return parseFloat(lastCell.innerHTML);
}

function getAllElevations() {
  let table = document.getElementById("height-zone-elevation-table");
  let elevations = [];
  if (table.rows.length === 1) {
    return elevations;
  }
  for (let i = 1; i < table.rows.length; i++) {
    elevations.push(parseFloat(table.rows[i].cells[1].innerHTML));
  }
  return elevations;
}

/**
 * Populate the default height zone elevation table
 */
function populateDefaultHeightZoneElevation() {
  let height = getHeight();

  if (height) {
    let numHeightZones = Math.ceil(height / 20);
    for (let j = 1; j < numHeightZones + 1; j++) {
      if (j === numHeightZones) {
        addHeightZoneElevationRow(height);
      } else {
        addHeightZoneElevationRow(j * 20);
      }
    }
  }
}

/**
 * Detect if height is changed and update the height zone elevation table
 */
function heightChange() {
  if (document.getElementById("number-height-zone-yes-option").checked) {
    clearHeightZoneElevationTable();
    populateDefaultHeightZoneElevation();
  } else if (document.getElementById("number-height-zone-no-option").checked) {
    // pass
  }
  if (document.getElementById("material-table") !== null) {
    heightZoneChange();
  }
}

/**
 * Detect if material weight is changed and update the material table
 */
function materialWeightChange() {
  if (document.getElementById("single-material-yes-option").checked === true) {
    let weight = document.getElementById("material-weight").value;
    clearMaterialTable();
    // iterate through the rows in the height zone elevation table
    let table = document.getElementById("height-zone-elevation-table");
    for (let i = 1; i < table.rows.length; i++) {
      addMaterialRow(weight);
    }
  }
}

/**
 * Detect if height zone is changed and update the material table
 */
function heightZoneChange() {
  let i;
  let table;
  if (document.getElementById("single-material-yes-option").checked === true) {
    let weight = document.getElementById("material-weight").value;
    clearMaterialTable();
    // iterate through the rows in the height zone elevation table
    table = document.getElementById("height-zone-elevation-table");
    for (i = 1; i < table.rows.length; i++) {
      addMaterialRow(weight);
    }
  } else if (
    document.getElementById("single-material-no-option").checked === true
  ) {
    clearMaterialTable();
    table = document.getElementById("height-zone-elevation-table");
    for (i = 1; i < table.rows.length; i++) {
      addMaterialRowEditable();
    }
  }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// MAP FUNCTIONS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Update the map with the given latitude, longitude, and address
 * @param latitude
 * @param longitude
 * @param address
 */
function setMap(latitude, longitude, address) {
  // If the map already exists, remove it
  if (MAP) {
    MAP.remove();
  }

  // Create a new map
  MAP = L.map("map", {
    attributionControl: false,
  }).setView([latitude, longitude], 13);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
  }).addTo(MAP);

  // Add a marker with a popup
  L.marker([latitude, longitude]).addTo(MAP).bindPopup(address);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// API CALLS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function stopLocationLoading() {
  document.getElementById("location_button").disabled = false;

  document
    .getElementById("location_button")
    .classList.remove("skeleton-loader");
  document
    .getElementById("wind-velocity-pressure")
    .classList.remove("skeleton-loader");
  document
    .getElementById("ground-snow-load")
    .classList.remove("skeleton-loader");
  document.getElementById("rain-load").classList.remove("skeleton-loader");
  document
    .getElementById("design-spectral-acceleration-0-2")
    .classList.remove("skeleton-loader");
  document
    .getElementById("design-spectral-acceleration-1")
    .classList.remove("skeleton-loader");

  document.getElementById("save-button").disabled = false;
}

/**
 * Computes location data based on the address, site designation, and seismic value in the backend
 * @param address
 * @param siteDesignation
 * @param seismicValue
 */
function locationCall(address, siteDesignation, seismicValue) {
  window.api.invoke("get-connection-address").then((connectionAddress) => {
    window.api
      .invoke("get-token") // Retrieve the token
      .then((token) => {
        let myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("Accept", "application/json");
        myHeaders.append("Authorization", `Bearer ${token}`);

        let raw = JSON.stringify({
          address: `${address}`,
          site_designation: `${siteDesignation}`,
          seismic_value: `${seismicValue}`,
        });

        let requestOptions = {
          method: "POST",
          headers: myHeaders,
          body: raw,
          redirect: "follow",
        };

        fetch(`${connectionAddress}/location`, requestOptions)
          .then((response) => response.json())
          .then((result) => {
            document.getElementById("wind-velocity-pressure").textContent =
              result.wind_velocity_pressure;
            document.getElementById("ground-snow-load").textContent =
              result.snow_load;
            document.getElementById("rain-load").textContent = result.rain_load;

            document.getElementById(
              "design-spectral-acceleration-0-2",
            ).textContent = result.design_spectral_acceleration_0_2;
            document.getElementById(
              "design-spectral-acceleration-1",
            ).textContent = result.design_spectral_acceleration_1;

            if (
              document.getElementById("wind-velocity-pressure").textContent ===
              ""
            ) {
              document.getElementById("wind-velocity-pressure").textContent =
                "NA";
              document.getElementById("ground-snow-load").textContent = "NA";
              document.getElementById("rain-load").textContent = "NA";
              document.getElementById(
                "design-spectral-acceleration-0-2",
              ).textContent = "NA";
              document.getElementById(
                "design-spectral-acceleration-1",
              ).textContent = "NA";

              setMap(-70.73964, -8.91217, "unknown");
              document.getElementById("location-error-message").innerText =
                "Please provide a more specific address. Perhaps use a postal code instead.";
              return;
            }

            // set the map as long as we have a valid latitude and longitude
            if (result.latitude && result.longitude) {
              document.getElementById("location-error-message").innerText = "";
              setMap(result.latitude, result.longitude, result.address);
            } else {
              document.getElementById("location-error-message").innerText =
                "Cannot find location, please try using a valid postal code instead";
              // set location variables to NA
              document.getElementById("wind-velocity-pressure").textContent =
                "NA";
              document.getElementById("ground-snow-load").textContent = "NA";
              document.getElementById("rain-load").textContent = "NA";
              document.getElementById(
                "design-spectral-acceleration-0-2",
              ).textContent = "NA";
              document.getElementById(
                "design-spectral-acceleration-1",
              ).textContent = "NA";
              setMap(-70.73964, -8.91217, "unknown");
            }

            document.getElementById("location_button").disabled = false;
          })
          .catch((error) => {
            console.error("Error:", error);
            stopLocationLoading();
          })
          .finally(() => {
            stopLocationLoading();
          });
      });
  });
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// BUTTON CLICK EVENTS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function startLoadingLocation(ids) {
  // disable button
  document.getElementById("location_button").disabled = true;

  ids.forEach((id) =>
    document.getElementById(id).classList.add("skeleton-loader"),
  );

  document.getElementById("save-button").disabled = true;
}

/**
 * Loads map and location data when the location button is clicked
 */
document
  .getElementById("location_button")
  .addEventListener("click", function () {
    const ids = [
      "location_button",
      "wind-velocity-pressure",
      "ground-snow-load",
      "rain-load",
      "design-spectral-acceleration-0-2",
      "design-spectral-acceleration-1",
    ];

    let address = getStrValue("address");
    let { siteDesignation, seismicValue } = getSeismicParameters();

    if (
      !(address === "" || siteDesignation === null || seismicValue === null)
    ) {
      startLoadingLocation(ids);

      locationCall(address, siteDesignation, seismicValue);
    }
  });

function startProcessingLoading() {
  // add skeleton loader to next button
  document.getElementById("next-button").classList.add("skeleton-loader");

  // add skeleton loader to all inputs on page
  document.querySelectorAll("input").forEach((input) => {
    input.classList.add("skeleton-loader");
  });

  // add skeleton loader to all tables on page
  document.querySelectorAll("table").forEach((table) => {
    table.classList.add("skeleton-loader");
  });

  // add skeleton loader to all cells in tables on page
  document.querySelectorAll("table td, table th").forEach((cell) => {
    cell.classList.add("skeleton-loader");
  });

  // add skeleton loader to all btn-secondary on page
  document.querySelectorAll(".btn-secondary").forEach((button) => {
    button.classList.add("skeleton-loader");
  });

  // add skeleton loader to all elements of type radio on page
  document.querySelectorAll('input[type="radio"]').forEach((radio) => {
    radio.disabled = true;
  });

  document.getElementById("save-button").disabled = true;
}

/**
 * When the next button is clicked, check that all fields are valid and then proceed to the next page
 */
document
  .getElementById("next-button")
  .addEventListener("click", async function () {
    await save();

    let defaultZones;
    if (document.getElementById("number-height-zone-yes-option").checked) {
      defaultZones = true;
    }

    // check that the project name is not empty
    if (document.getElementById("project-name").value === "") {
      document.getElementById("next-warning").innerText =
        "Please enter a project name";
    }

    // check that the address is not empty
    else if (document.getElementById("address").value === "") {
      document.getElementById("next-warning").innerText =
        "Please enter an address";
    }

    // check that a site designation type is selected
    else if (
      document
        .getElementById("site-designation-selection")
        .querySelector(".selected") === null
    ) {
      document.getElementById("next-warning").innerText =
        "Please select a site designation type";
    }

    // if the site designation type is vs30, check that the vs30 value is not empty
    else if (
      document.getElementById("vs30_option").checked &&
      document.getElementById("vs30").value === ""
    ) {
      document.getElementById("next-warning").innerText =
        "Please enter a vs30 value";
    }

    // check that vs30 is in the range [140, 3000] inclusive
    else if (
      document.getElementById("vs30_option").checked &&
      (parseFloat(document.getElementById("vs30").value) < 140 ||
        parseFloat(document.getElementById("vs30").value) > 3000)
    ) {
      document.getElementById("next-warning").innerText =
        "vs30 must be in the range [140, 3000]";
    }

    // if the site designation type is xs, check that an xs type is selected
    else if (
      document.getElementById("xs_option").checked &&
      document
        .getElementById("xs-type-selection")
        .querySelector(".selected") === null
    ) {
      document.getElementById("next-warning").innerText =
        "Please select an xs type";
    }

    // if the wind, snow, rain, design spectral acceleration 0.2, and design spectral acceleration 1 values are not set
    else if (
      document.getElementById("wind-velocity-pressure").textContent === "NA" ||
      document.getElementById("ground-snow-load").textContent === "NA" ||
      document.getElementById("rain-load").textContent === "NA" ||
      document.getElementById("design-spectral-acceleration-0-2")
        .textContent === "NA" ||
      document.getElementById("design-spectral-acceleration-1").textContent ===
        "NA"
    ) {
      document.getElementById("next-warning").innerText =
        "Ensure the location button has been clicked and the values have been retrieved. If values cannot be retrieved, then you have entered an invalid address";
    } else if (
      document.getElementById("wind-velocity-pressure").textContent === "" ||
      document.getElementById("ground-snow-load").textContent === "" ||
      document.getElementById("rain-load").textContent === "" ||
      document.getElementById("design-spectral-acceleration-0-2")
        .textContent === "" ||
      document.getElementById("design-spectral-acceleration-1").textContent ===
        ""
    ) {
      document.getElementById("next-warning").innerText =
        "Ensure the location button has been clicked and the values have been retrieved. If values cannot be retrieved, then you have entered an invalid address";
    }

    // if the building width is not set
    else if (document.getElementById("width").value === "") {
      document.getElementById("next-warning").innerText =
        "Please enter a building width";
    }

    // if the eave and ridge selection is not set
    else if (
      document
        .getElementById("eave-and-ridge-selection")
        .querySelector(".selected") === null
    ) {
      document.getElementById("next-warning").innerText =
        "Please select an eave and ridge option";
    }

    // if the eave and ridge selection is yes, check that the eave height and ridge height are not empty
    else if (
      document.getElementById("eave-and-ridge-yes-option").checked &&
      (document.getElementById("eave-height").value === "" ||
        document.getElementById("ridge-height").value === "")
    ) {
      document.getElementById("next-warning").innerText =
        "Please enter an eave and ridge height";
    }

    // if the eave and ridge selection is yes, check that height is not empty
    else if (
      document.getElementById("eave-and-ridge-no-option").checked &&
      document.getElementById("height").value === ""
    ) {
      document.getElementById("next-warning").innerText =
        "Please enter a height";
    }

    // check that the number of floors is not empty
    else if (document.getElementById("num-floors").value === "") {
      document.getElementById("next-warning").innerText =
        "Please enter the number of floors";
    }

    // check that the top of cladding it not empty
    else if (document.getElementById("top-cladding").value === "") {
      document.getElementById("next-warning").innerText =
        "Please enter the top of cladding";
    }

    // check that bottom of cladding is not empty
    else if (document.getElementById("bottom-cladding").value === "") {
      document.getElementById("next-warning").innerText =
        "Please enter the bottom of cladding";
    }

    // if the dominant opening selection is not set
    else if (
      document
        .getElementById("dominant-opening-selection")
        .querySelector(".selected") === null
    ) {
      document.getElementById("next-warning").innerText =
        "Please select a dominant opening option";
    }

    // if the dominant opening selection is yes, check that the mid-height is not empty
    else if (
      document.getElementById("dominant-opening-yes-option").checked &&
      document.getElementById("mid-height").value === ""
    ) {
      document.getElementById("next-warning").innerText =
        "Please enter a mid-height";
    }

    // check that w-roof is not empty
    else if (document.getElementById("w-roof").value === "") {
      document.getElementById("next-warning").innerText = "Please enter w-roof";
    }

    // check that l-roof is not empty
    else if (document.getElementById("l-roof").value === "") {
      document.getElementById("next-warning").innerText = "Please enter l-roof";
    }

    // check that a-roof is not empty
    else if (document.getElementById("a-roof").value === "") {
      document.getElementById("next-warning").innerText = "Please enter a-roof";
    }

    // check that a-roof is in the range [0, 360] inclusive
    else if (
      parseFloat(document.getElementById("a-roof").value) < 0 ||
      parseFloat(document.getElementById("a-roof").value) > 360
    ) {
      document.getElementById("next-warning").innerText =
        "a-roof must be in the range [0, 360]";
    }

    // check that roof-uniform-dead-load is not empty
    else if (document.getElementById("roof-uniform-dead-load").value === "") {
      document.getElementById("next-warning").innerText =
        "Please enter roof uniform dead load";
    }

    // check that an importance category is selected
    else if (
      document
        .getElementById("importance-category-selection")
        .querySelector(".selected") === null
    ) {
      document.getElementById("next-warning").innerText =
        "Please select an importance category";
    }

    // check that number of height zones is selected
    else if (
      document
        .getElementById("number-height-zone-selection")
        .querySelector(".selected") === null
    ) {
      document.getElementById("next-warning").innerText =
        "Please select a number of height zones option";
    }

    // check that a material type is selected
    else if (
      document
        .getElementById("single-material-selection")
        .querySelector(".selected") === null
    ) {
      document.getElementById("next-warning").innerText =
        "Please select whether or not a single material will be applied to all height zones";
    }

    // if single material is selected, check that the material weight is not empty
    else if (
      document.getElementById("single-material-yes-option").checked &&
      document.getElementById("material-weight").value === ""
    ) {
      document.getElementById("next-warning").innerText =
        "Please enter a material weight";
    }

    // TODO: if no check
    else if (
      document.getElementById("height-zone-elevation-table").rows.length !==
      document.getElementById("material-table").rows.length
    ) {
      document.getElementById("next-warning").innerText =
        "The number of height zones in both tables must be the same";
    }

    // ensure that the tallest elevation is equal to the building height
    else if (parseFloat(getHeight()) !== getTallestElevation()) {
      console.log(getHeight());
      console.log(getTallestElevation());
      document.getElementById("next-warning").innerText =
        "The tallest elevation must be equal to the building height";
    } else if (!ascending(getAllElevations())) {
      document.getElementById("next-warning").innerText =
        "The elevations must be in ascending order";
    } else {
      document.getElementById("next-warning").innerText =
        "Processing data, please wait...";
      document.getElementById("next-warning").style.color = "#9bca6d";

      startProcessingLoading();

      window.api.invoke("get-connection-address").then((connectionAddress) => {
        window.api
          .invoke("get-token") // Retrieve the token
          .then((token) => {
            // LOCATION
            let address = getStrValue("address");
            let { siteDesignation, seismicValue } = getSeismicParameters();

            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Accept", "application/json");
            myHeaders.append("Authorization", `Bearer ${token}`);

            const raw = JSON.stringify({
              address: `${address}`,
              site_designation: `${siteDesignation}`,
              seismic_value: `${seismicValue}`,
            });

            const requestOptions = {
              method: "POST",
              headers: myHeaders,
              body: raw,
              redirect: "follow",
            };

            fetch(`${connectionAddress}/location`, requestOptions)
              .then((response) => {
                // DIMENSIONS
                if (response.status === 200) {
                  let width = getFloatValue("width");
                  let eaveHeight = getFloatValue("eave-height");
                  let ridgeHeight = getFloatValue("ridge-height");
                  let height = getFloatValue("height");

                  const myHeaders = new Headers();
                  myHeaders.append("Content-Type", "application/json");
                  myHeaders.append("Accept", "application/json");
                  myHeaders.append("Authorization", `Bearer ${token}`);

                  const raw = JSON.stringify({
                    width: width,
                    height: height,
                    eave_height: eaveHeight,
                    ridge_height: ridgeHeight,
                  });

                  const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow",
                  };

                  fetch(`${connectionAddress}/dimensions`, requestOptions)
                    .then((response) => {
                      // CLADDING
                      if (response.status === 200) {
                        let cTop = getFloatValue("top-cladding");
                        let cBot = getFloatValue("bottom-cladding");

                        const myHeaders = new Headers();
                        myHeaders.append("Content-Type", "application/json");
                        myHeaders.append("Accept", "application/json");
                        myHeaders.append("Authorization", `Bearer ${token}`);

                        const raw = JSON.stringify({
                          c_top: cTop,
                          c_bot: cBot,
                        });

                        const requestOptions = {
                          method: "POST",
                          headers: myHeaders,
                          body: raw,
                          redirect: "follow",
                        };

                        fetch(`${connectionAddress}/cladding`, requestOptions)
                          .then((response) => {
                            // ROOF
                            if (response.status === 200) {
                              let wRoof = getFloatValue("w-roof");
                              let lRoof = getFloatValue("l-roof");
                              let aRoof = getFloatValue("a-roof");
                              let roofUniformDeadLoad = getFloatValue(
                                "roof-uniform-dead-load",
                              );

                              const myHeaders = new Headers();
                              myHeaders.append(
                                "Content-Type",
                                "application/json",
                              );
                              myHeaders.append("Accept", "application/json");
                              myHeaders.append(
                                "Authorization",
                                `Bearer ${token}`,
                              );

                              const raw = JSON.stringify({
                                w_roof: wRoof,
                                l_roof: lRoof,
                                slope: aRoof,
                                uniform_dead_load: roofUniformDeadLoad,
                              });

                              const requestOptions = {
                                method: "POST",
                                headers: myHeaders,
                                body: raw,
                                redirect: "follow",
                              };

                              fetch(`${connectionAddress}/roof`, requestOptions)
                                .then((response) => {
                                  // BUILDING
                                  if (response.status === 200) {
                                    let numFloors = getIntValue("num-floors");
                                    let midHeight = getFloatValue("mid-height");

                                    // list of tuples of the form (height, elevation)
                                    let zones = [];
                                    // list of tuples of the form (height, load)
                                    let materials = [];
                                    // iterate through height zone elevation table data rows
                                    let heightZoneElevationTable =
                                      document.getElementById(
                                        "height-zone-elevation-table",
                                      );
                                    let materialTable =
                                      document.getElementById("material-table");

                                    for (
                                      let i = 1;
                                      i < heightZoneElevationTable.rows.length;
                                      i++
                                    ) {
                                      let zoneNum = parseInt(
                                        heightZoneElevationTable.rows[i]
                                          .cells[0].innerHTML,
                                      );
                                      let elevation = parseFloat(
                                        heightZoneElevationTable.rows[i]
                                          .cells[1].innerHTML,
                                      );
                                      let load = parseFloat(
                                        materialTable.rows[i].cells[1]
                                          .innerHTML,
                                      );
                                      zones.push([zoneNum, elevation]);
                                      materials.push([zoneNum, load]);
                                    }

                                    const myHeaders = new Headers();
                                    myHeaders.append(
                                      "Content-Type",
                                      "application/json",
                                    );
                                    myHeaders.append(
                                      "Accept",
                                      "application/json",
                                    );
                                    myHeaders.append(
                                      "Authorization",
                                      `Bearer ${token}`,
                                    );

                                    console.log(defaultZones);

                                    if (defaultZones === true) {
                                      zones = null;
                                    }

                                    const raw = JSON.stringify({
                                      num_floor: numFloors,
                                      h_opening: midHeight,
                                      zones: zones,
                                      materials: materials,
                                    });

                                    const requestOptions = {
                                      method: "POST",
                                      headers: myHeaders,
                                      body: raw,
                                      redirect: "follow",
                                    };

                                    fetch(
                                      `${connectionAddress}/building`,
                                      requestOptions,
                                    )
                                      .then((response) => {
                                        // IMPORTANCE CATEGORY
                                        if (response.status === 200) {
                                          let importance_category = null;
                                          // if low is checked
                                          if (
                                            document.getElementById(
                                              "importance-category-low-option",
                                            ).checked
                                          ) {
                                            importance_category = "LOW";
                                          }
                                          // if normal is checked
                                          else if (
                                            document.getElementById(
                                              "importance-category-normal-option",
                                            ).checked
                                          ) {
                                            importance_category = "NORMAL";
                                          } else if (
                                            document.getElementById(
                                              "importance-category-high-option",
                                            ).checked
                                          ) {
                                            importance_category = "HIGH";
                                          }

                                          // if post disaster is checked
                                          else if (
                                            document.getElementById(
                                              "importance-category-post-disaster-option",
                                            ).checked
                                          ) {
                                            importance_category =
                                              "POST_DISASTER";
                                          }

                                          const myHeaders = new Headers();
                                          myHeaders.append(
                                            "Content-Type",
                                            "application/json",
                                          );
                                          myHeaders.append(
                                            "Accept",
                                            "application/json",
                                          );
                                          myHeaders.append(
                                            "Authorization",
                                            `Bearer ${token}`,
                                          );

                                          const raw = JSON.stringify({
                                            importance_category:
                                              importance_category,
                                          });

                                          const requestOptions = {
                                            method: "POST",
                                            headers: myHeaders,
                                            body: raw,
                                            redirect: "follow",
                                          };

                                          fetch(
                                            `${connectionAddress}/importance_category`,
                                            requestOptions,
                                          )
                                            .then((response) => {
                                              if (response.status === 200) {
                                                window.location.href =
                                                  "load.html";
                                              } else {
                                                throw new Error(
                                                  "importance category error",
                                                );
                                              }
                                            })
                                            .catch((error) =>
                                              console.error(error),
                                            );
                                        } else {
                                          throw new Error("building error");
                                        }
                                      })
                                      .catch((error) => console.error(error));
                                  } else {
                                    throw new Error("roof error");
                                  }
                                })
                                .catch((error) => console.error(error));
                            } else {
                              throw new Error("cladding error");
                            }
                          })
                          .catch((error) => console.error(error));
                      } else {
                        throw new Error("dimensions error");
                      }
                    })
                    .catch((error) => console.error(error));
                } else {
                  throw new Error("location error");
                }
              })
              .catch((error) => console.error(error));
          });
      });
    }
  });

function save() {
  return window.api
    .invoke("get-connection-address")
    .then((connectionAddress) => {
      return window.api
        .invoke("get-token") // Retrieve the token
        .then((token) => {
          const myHeaders = new Headers();
          myHeaders.append("Accept", "application/json");
          myHeaders.append("Authorization", `Bearer ${token}`);

          const requestOptions = {
            method: "POST",
            headers: myHeaders,
            redirect: "follow",
          };

          return fetch(
            `${connectionAddress}/get_user_current_save_file`,
            requestOptions,
          )
            .then((response) => {
              if (response.status === 200) {
                return response.json();
              } else {
                throw new Error("Get User Current Save File Error");
              }
            })
            .then((result) => {
              let id = parseInt(result);
              const myHeaders = new Headers();
              myHeaders.append("Content-Type", "application/json");
              myHeaders.append("Accept", "application/json");
              myHeaders.append("Authorization", `Bearer ${token}`);

              const raw = JSON.stringify({
                json_data: serialize(),
                id: id,
              });

              const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow",
              };

              return fetch(
                `${connectionAddress}/set_user_save_data`,
                requestOptions,
              )
                .then((response) => response.text())
                .catch((error) => console.error(error));
            })
            .catch((error) => console.error(error));
        });
    });
}

/**
 * When the save button is clicked, serialize the input page and send it to the backend
 */
document
  .getElementById("save-button")
  .addEventListener("click", async function () {
    await save();
  });

/**
 * When the back button is clicked, return to the home page
 */
document
  .getElementById("back-button")
  .addEventListener("click", async function () {
    await save();
    window.location.href = "home.html";
  });

/**
 * When the building view button is clicked, send the input data to the backend and display the rendered building
 */
document
  .getElementById("building-view-button")
  .addEventListener("click", function () {
    window.api.invoke("get-connection-address").then((connectionAddress) => {
      window.api
        .invoke("get-token") // Retrieve the token
        .then((token) => {
          const myHeaders = new Headers();
          myHeaders.append("Content-Type", "application/json");
          myHeaders.append("Accept", "application/json");
          myHeaders.append("Authorization", `Bearer ${token}`);

          let totalElevation = getHeight();
          let roofAngle = getFloatValue("a-roof");

          const raw = JSON.stringify({
            total_elevation: totalElevation,
            roof_angle: roofAngle,
          });

          const requestOptions = {
            method: "POST",
            headers: myHeaders,
            body: raw,
            redirect: "follow",
          };

          document.getElementById("building-render-error").style.display =
            "block";
          document.getElementById("building-render-error").innerHTML =
            "You have been placed in a rendering queue. Please wait for the render to complete...";

          document.getElementById("building-render-info").style.display =
            "none";
          document.getElementById("building-render-info").innerHTML = "";

          fetch(`${connectionAddress}/simple_model`, requestOptions)
            .then((response) => response.json())
            .then((result) => {
              let id = JSON.parse(result);

              let img = document.createElement("img");
              setSimpleModelImage(connectionAddress, id, img);

              document.getElementById("building-render-error").style.display =
                "none";
              document.getElementById("building-render-error").innerHTML = "";

              document.getElementById("building-render-info").style.display =
                "block";
              document.getElementById("building-render-info").innerHTML =
                `Total Elevation: ${totalElevation} m, Roof Angle: ${roofAngle}°`;
            })
            .catch((error) => {
              console.error(error);
              document.getElementById("building-render-error").style.display =
                "block";
              document.getElementById("building-render-error").innerHTML =
                "Render failed. Please try again.";

              document.getElementById("building-render-info").style.display =
                "none";
              document.getElementById("building-render-info").innerHTML = "";
            });
        });
    });
  });

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SERIALIZATION
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Serialize the input page
 * @returns A JSON string representing the input page
 */
function serialize() {
  let objects = {
    input_page: {
      radio: {},
      input: {},
      table: {},
    },
  };

  // Handle radio inputs
  let radios = document.querySelectorAll("input[type=radio]");
  radios.forEach((radio) => {
    if (radio.checked) {
      objects.input_page.radio[radio.id] = radio.value;
    }
  });

  // Handle other inputs
  let inputs = document.querySelectorAll("input:not([type=radio])");
  inputs.forEach((input) => {
    if (input.value !== "") {
      objects.input_page.input[input.id] = input.value;
    }
  });

  // Handle tables
  let tables = document.querySelectorAll("table");
  tables.forEach((table) => {
    objects.input_page.table[table.id] = table.innerHTML;
  });

  let json = JSON.stringify(objects);
  return json;
}

/**
 * wait for an element with the given id to appear
 * @param id
 * @param callback
 */
function waitForElement(id, callback) {
  let intervalId = setInterval(function () {
    let element = document.getElementById(id);
    if (element) {
      clearInterval(intervalId);
      callback(element);
    }
  }, 100); // Check every 100ms
}

/**
 * Deserialize the input page
 * @param json
 * @param section
 * @returns {Promise<unknown>}
 */
function deserialize(json, section) {
  return new Promise((resolve) => {
    let objects = JSON.parse(json)[section];
    let totalElements =
      Object.keys(objects.radio).length +
      Object.keys(objects.input).length +
      Object.keys(objects.table).length;
    let processedElements = 0;

    // go through all the radio
    for (let id in objects.radio) {
      waitForElement(id, function (radio) {
        if (radio.value === objects.radio[id]) {
          radio.click();
        }
        processedElements++;
        if (processedElements === totalElements) {
          resolve();
        }
      });
    }

    // go through all the input
    for (let id in objects.input) {
      waitForElement(id, function (input) {
        input.value = "";
        input.focus();
        let value = objects.input[id];
        for (let i = 0; i < value.length; i++) {
          input.value = value;
        }
        processedElements++;
        if (processedElements === totalElements) {
          resolve();
        }
      });
    }

    // go through all the tables
    for (let id in objects.table) {
      waitForElement(id, function (table) {
        table.innerHTML = objects.table[id];
        processedElements++;
        if (processedElements === totalElements) {
          resolve();
        }
      });
    }
  });
}

/**
 * Load the save file
 */
function loadSaveFile() {
  window.api.invoke("get-connection-address").then((connectionAddress) => {
    window.api
      .invoke("get-token") // Retrieve the token
      .then((token) => {
        const myHeaders = new Headers();
        myHeaders.append("Accept", "application/json");
        myHeaders.append("Authorization", `Bearer ${token}`);

        const requestOptions = {
          method: "POST",
          headers: myHeaders,
          redirect: "follow",
        };

        fetch(`${connectionAddress}/get_user_current_save_file`, requestOptions)
          .then((response) => {
            if (response.status === 200) {
              return response.json();
            } else {
              throw new Error("Get User Current Save File Error");
            }
          })
          .then((result) => {
            let id = parseInt(result);
            const myHeaders = new Headers();
            myHeaders.append("Accept", "application/json");
            myHeaders.append("Authorization", `Bearer ${token}`);

            const requestOptions = {
              method: "POST",
              headers: myHeaders,
              redirect: "follow",
            };

            fetch(
              `${connectionAddress}/get_user_save_file?id=${id}`,
              requestOptions,
            )
              .then((response) => {
                if (response.status === 200) {
                  return response.json();
                } else {
                  throw new Error("Get User Save File Error");
                }
              })
              .then((data) => {
                const myHeaders = new Headers();
                myHeaders.append("Accept", "application/json");
                myHeaders.append("Authorization", `Bearer ${token}`);

                const requestOptions = {
                  method: "POST",
                  headers: myHeaders,
                  redirect: "follow",
                };

                fetch(
                  `${connectionAddress}/get_user_save_file?id=${id}`,
                  requestOptions,
                )
                  .then((response) => {
                    if (response.status === 200) {
                      return response.json();
                    } else {
                      throw new Error("Get User Save File Error");
                    }
                  })
                  .then((result) => {
                    deserialize(result.JsonData, "input_page").then(() => {
                      window.scrollTo(0, 0);
                    });
                  })
                  .catch((error) => {
                    console.error(error);
                    window.reload();
                  });
              })
              .catch((error) => {
                console.error(error);
                window.reload();
              });
          })
          .catch((error) => {
            console.error(error);
            window.reload();
          });
      });
  });
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// DROPDOWN MENU
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Set the username in the dropdown menu
 */
function setUsernameDropdown() {
  window.api.invoke("get-connection-address").then((connectionAddress) => {
    window.api
      .invoke("get-token") // Retrieve the token
      .then((token) => {
        const myHeaders = new Headers();
        myHeaders.append("Accept", "application/json");
        myHeaders.append("Authorization", `Bearer ${token}`);

        const requestOptions = {
          method: "POST",
          headers: myHeaders,
          redirect: "follow",
        };

        fetch(`${connectionAddress}/get_user_profile`, requestOptions)
          .then((response) => response.json())
          .then((result) => {
            let data = JSON.parse(result);
            username = data["username"];
            document.getElementById("navbarDropdownMenuLink").textContent =
              username;
          })
          .catch((error) => (window.location.href = "login.html"));
      });
  });
}

/**
 * If clicked the user will be logged out and redirected to the login page
 */
document.getElementById("logout").addEventListener("click", function () {
  window.api.invoke("store-token", "");
  window.location.href = "login.html";
});

/**
 * If clicked the user will be redirected to the profile page */
document.getElementById("profile").addEventListener("click", function () {
  window.location.href = "profile.html";
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// WINDOW ONLOAD EVENT
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Set up the page on load
 */
window.onload = function () {
  setUsernameDropdown();
  loadSaveFile();

  setMap(43.66074, -79.39661, "Myhal Centre, Toronto, Ontario, Canada");

  const selectors = [
    "#site-designation-selection",
    "#eave-and-ridge-selection",
    "#number-height-zone-selection",
    "#dominant-opening-selection",
    "#single-material-selection",
    "#importance-category-selection",
  ];

  selectors.forEach((selector) => toggleMenuColors(selector));

  siteDesignationSelection();
  eaveAndRidgeSelection();
  numberHeightZoneSelection();
  dominantOpeningSelection();
  materialSelection();
};
