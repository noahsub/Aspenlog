////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// results.js
// This file contains the scripts for the results page.
//
// Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code
// By using this code, you agree to abide by the terms and conditions in those files.
//
// Author: Noah Subedar [https://github.com/noahsub]
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// CONSTANTS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

let ULS_WALL_SELECTION;
let SLS_WALL_SELECTION;
let ULS_ROOF_SELECTION;
let SLS_ROOF_SELECTION;

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// HELPER FUNCTIONS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * changes the color of the selected button in a toggle menu
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
 * Sets the wind load model image, if the image is not found, it will attempt to fetch the image again
 * @param connectionAddress
 * @param id
 * @param attempt
 */
function setWindLoadModelImage(connectionAddress, id, attempt = 10) {
  fetch(`${connectionAddress}/get_wind_load_model?id=${id}`)
    .then((response) => {
      if (response.status === 200) {
        document.getElementById("wind-load-image").src =
          `${connectionAddress}/get_wind_load_model?id=${id}`;
      } else {
        if (attempt > 0) {
          return setWindLoadModelImage(connectionAddress, id, attempt - 1);
        } else {
          throw new Error("Wind Load Image Not Found");
        }
      }
    })
    .catch((error) => console.error(error));
}

/**
 * Sets the seismic load model image, if the image is not found, it will attempt to fetch the image again
 * @param connectionAddress
 * @param id
 * @param attempt
 */
function setSeismicLoadModelImage(connectionAddress, id, attempt = 10) {
  fetch(`${connectionAddress}/get_seismic_load_model?id=${id}`)
    .then((response) => {
      if (response.status === 200) {
        document.getElementById("seismic-load-image").src =
          `${connectionAddress}/get_seismic_load_model?id=${id}`;
      } else {
        if (attempt > 0) {
          return setWindLoadModelImage(connectionAddress, id, attempt - 1);
        } else {
          throw new Error("Seismic Load Image Not Found");
        }
      }
    })
    .catch((error) => console.error(error));
}

/**
 * Sets the bar chart image, if the image is not found, it will attempt to fetch the image again
 * @param connectionAddress
 * @param id
 * @param i
 * @param img
 * @param position
 * @param attempt
 */
function setBarChartImage(
  connectionAddress,
  id,
  i,
  img,
  position,
  attempt = 10,
) {
  fetch(`${connectionAddress}/get_bar_chart?id=${id}&zone_num=${i + 1}`)
    .then((response) => {
      if (response.status === 200) {
        img.src = `${connectionAddress}/get_bar_chart?id=${id}&zone_num=${i + 1}`;
        img.style.maxWidth = "100%";

        if (position === "left") {
          document.getElementById("left-bar-chart-container").appendChild(img);
        } else if (position === "middle") {
          document
            .getElementById("middle-bar-chart-container")
            .appendChild(img);
        } else if (position === "right") {
          document.getElementById("right-bar-chart-container").appendChild(img);
        }
      } else {
        if (attempt > 0) {
          return setBarChartImage(
            connectionAddress,
            id,
            i,
            img,
            position,
            attempt - 1,
          );
        } else {
          throw new Error("Bar Chart Image Not Found");
        }
      }
    })
    .catch((error) => console.error(error));
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SERIALIZATION
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Wait for an element to load
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
                    // if there is no data to deserialize we still want to generate the load model
                    // and bar chart
                    deserialize(result.JsonData, "result_page")
                      .then(() => {
                        generate_load_model();
                        generate_bar_chart();
                        window.scrollTo(0, 0);
                      })
                      .catch((error) => {
                        generate_load_model();
                        generate_bar_chart();
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

/**
 * Serialize the current state of the page
 * @returns {string}
 */
function serialize() {
  let objects = {
    result_page: {
      radio: {},
      input: {},
    },
  };

  // Handle radio inputs
  let radios = document.querySelectorAll("input[type=radio]");
  radios.forEach((radio) => {
    if (radio.checked) {
      objects.result_page.radio[radio.id] = radio.value;
    }
  });

  let json = JSON.stringify(objects);
  return json;
}

/**
 * Deserialize the current state of the page
 * @param json
 * @param section
 * @returns {Promise<unknown>}
 */
function deserialize(json, section) {
  return new Promise((resolve) => {
    let objects = JSON.parse(json)[section];
    let totalElements =
      Object.keys(objects.radio).length + Object.keys(objects.input).length;
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
  });
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// BUTTON CLICK EVENTS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
 * When the save button is clicked, the current state of the page is serialized and sent to the backend to be saved.
 */
document.getElementById("save-button").addEventListener("click", async () => {
  await save();
});

/**
 * When the back button is clicked, the user is redirected to the load page.
 */
document
  .getElementById("uls-wall-selection")
  .addEventListener("change", function (e) {
    let selectedOption = e.target.id;
    switch (selectedOption) {
      case "uls-wall-selection-dead-only-1-4D-option":
        ULS_WALL_SELECTION = "uls_1.4D";
        break;
      case "uls-wall-selection-full-wind-1-25D-1-4Wy-option":
        ULS_WALL_SELECTION = "uls_1.25D_1.4Wy";
        break;
      case "uls-wall-selection-seismic-1-0D-1-0Ey-option":
        ULS_WALL_SELECTION = "uls_1.0D_1.0Ey";
        break;
      case "uls-wall-selection-seismic-1-0D-1-0Ex-option":
        ULS_WALL_SELECTION = "uls_1.0D_1.0Ex";
        break;
    }

    if (ULS_WALL_SELECTION !== undefined && SLS_WALL_SELECTION !== undefined) {
      getWallLoadCombinations();
    }
  });

/**
 * When the back button is clicked, the user is redirected to the load page.
 */
document.getElementById("back-button").addEventListener("click", async () => {
  await save();
  window.location.href = "load.html";
});

/**
 * When the back home is clicked, the user is redirected to the home page.
 */
document
  .getElementById("home-button")
  .addEventListener("click", async function () {
    await save();
    window.location.href = "home.html";
  });

document
  .getElementById("export-button")
  .addEventListener("click", async function () {
    await save();

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

          fetch(`${connectionAddress}/excel_output`, requestOptions)
            .then((response) => {
              // Get filename from Content-Disposition header
              const contentDisposition = response.headers.get(
                "Content-Disposition",
              );
              let filename = "default_filename.extension";
              if (contentDisposition) {
                const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                let matches = filenameRegex.exec(contentDisposition);
                if (matches != null && matches[1]) {
                  filename = matches[1].replace(/['"]/g, "");
                }
              }

              return response.blob().then((blob) => ({ blob, filename }));
            })
            .then(({ blob, filename }) => {
              // Convert blob to buffer
              blob.arrayBuffer().then((buffer) => {
                // Convert ArrayBuffer to Uint8Array
                const uint8Array = new Uint8Array(buffer);
                // Send Uint8Array and filename to main process for writing to file
                window.api.invoke("download", { data: uint8Array, filename });
              });

              document.getElementById("export-warning").innerText =
                `Downloaded ${filename}`;

              setTimeout(function () {
                document.getElementById("export-warning").innerText = "";
              }, 5000);
            })
            .catch((error) => console.error(error));
        });
    });
  });

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SELECTION CHANGE EVENTS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * When the wall selection is changed, the load combinations are updated.
 */
document
  .getElementById("sls-wall-selection")
  .addEventListener("change", function (e) {
    let selectedOption = e.target.id;
    switch (selectedOption) {
      case "sls-wall-selection-1-0D-1-0Wy-option":
        SLS_WALL_SELECTION = "sls_1.0D_1.0Wy";
        break;
    }

    if (ULS_WALL_SELECTION !== undefined && SLS_WALL_SELECTION !== undefined) {
      getWallLoadCombinations();
    }
  });

/**
 * When the roof selection is changed, the load combinations are updated.
 */
document
  .getElementById("uls-roof-selection")
  .addEventListener("change", function (e) {
    let selectedOption = e.target.id;
    switch (selectedOption) {
      case "uls-roof-selection-dead-only-1-4D-option":
        ULS_ROOF_SELECTION = "uls_1.4D";
        break;
      case "uls-roof-selection-full-wind-1-25D-1-4Wy-option":
        ULS_ROOF_SELECTION = "uls_1.25D_1.4Wy";
        break;
      case "uls-roof-selection-seismic-1-0D-1-0Ey-option":
        ULS_ROOF_SELECTION = "uls_1.0D_1.0Ey";
        break;
      case "uls-roof-selection-seismic-1-0D-1-0Ex-option":
        ULS_ROOF_SELECTION = "uls_1.0D_1.0Ex";
        break;
      case "uls-roof-selection-full-snow-with-wind-1-25D-1-5S-option":
        ULS_ROOF_SELECTION = "uls_1.25D_1.5S";
        break;
    }

    if (ULS_ROOF_SELECTION !== undefined && SLS_ROOF_SELECTION !== undefined) {
      getRoofLoadCombinations();
    }
  });

/**
 * When the roof selection is changed, the load combinations are updated.
 */
document
  .getElementById("sls-roof-selection")
  .addEventListener("change", function (e) {
    let selectedOption = e.target.id;
    switch (selectedOption) {
      case "sls-roof-selection-dead-and-wind-y-normal-to-face-1-0D-1-0Wy-option":
        SLS_ROOF_SELECTION = "sls_1.0D_1.0Wy";
        break;
      case "sls-roof-selection-full-snow-with-wind-y-1-0D-1-0S-option":
        SLS_ROOF_SELECTION = "sls_1.0D_1.0S";
        break;
      case "sls-roof-selection-dead-and-live-1-0D-1-0L-option":
        SLS_ROOF_SELECTION = "sls_1.0D_1.0L_WY";
        break;
    }

    if (ULS_ROOF_SELECTION !== undefined && SLS_ROOF_SELECTION !== undefined) {
      getRoofLoadCombinations();
    }
  });

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// GET LOAD COMBINATIONS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function startWallCombinationLoading() {
  for (
    let row = 0;
    row < document.getElementById("wall-combination-table").rows.length;
    row++
  ) {
    for (
      let cell = 0;
      cell <
      document.getElementById("wall-combination-table").rows[row].cells.length;
      cell++
    ) {
      document
        .getElementById("wall-combination-table")
        .rows[row].cells[cell].classList.add("skeleton-loader");
    }
  }

  document.getElementById("save-button").disabled = true;
}

function stopWallCombinationLoading() {
  for (
    let row = 0;
    row < document.getElementById("wall-combination-table").rows.length;
    row++
  ) {
    for (
      let cell = 0;
      cell <
      document.getElementById("wall-combination-table").rows[row].cells.length;
      cell++
    ) {
      document
        .getElementById("wall-combination-table")
        .rows[row].cells[cell].classList.remove("skeleton-loader");
    }
  }

  document.getElementById("save-button").disabled = false;
}

/**
 * Get the wall load combinations
 */
function getWallLoadCombinations() {
  window.api.invoke("get-connection-address").then((connectionAddress) => {
    window.api
      .invoke("get-token") // Retrieve the token
      .then((token) => {
        const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("Accept", "application/json");
        myHeaders.append("Authorization", `Bearer ${token}`);

        const raw = JSON.stringify({
          uls_wall_type: ULS_WALL_SELECTION,
          sls_wall_type: SLS_WALL_SELECTION,
        });

        const requestOptions = {
          method: "POST",
          headers: myHeaders,
          body: raw,
          redirect: "follow",
        };

        startWallCombinationLoading();

        fetch(`${connectionAddress}/get_wall_load_combinations`, requestOptions)
          .then((response) => response.text())
          .then((result) => {
            let data = JSON.parse(result);
            let table = document.getElementById("wall-combination-table");
            table.innerHTML = "";
            let tableString = "";
            tableString += "<thead>";
            tableString += "<tr>";
            let headers = Object.keys(data[0]);
            tableString += `<th>Height Zone</th>`;
            headers.forEach((header) => {
              tableString += `<th>${header}</th>`;
            });
            tableString += "<tr>";
            tableString += "</thead>";
            tableString += "<tbody>";
            for (let i = 0; i < data.length; i++) {
              tableString += "<tr>";
              let values = Object.values(data[i]);
              let newValues = [i + 1].concat(values);
              newValues.forEach((value) => {
                tableString += `<td>${value}</td>`;
              });
              tableString += "</tr>";
            }
            tableString += "</tbody>";
            table.innerHTML = tableString;

            stopWallCombinationLoading();
          })
          .catch((error) => {
            console.error(error);
            stopWallCombinationLoading();
          });
      });
  });
}

function startRoofCombintaionLoading() {
  for (
    let row = 0;
    row < document.getElementById("roof-combination-table").rows.length;
    row++
  ) {
    for (
      let cell = 0;
      cell <
      document.getElementById("roof-combination-table").rows[row].cells.length;
      cell++
    ) {
      document
        .getElementById("roof-combination-table")
        .rows[row].cells[cell].classList.add("skeleton-loader");
    }
  }

  document.getElementById("save-button").disabled = true;
}

function stopRoofCombinationLoading() {
  for (
    let row = 0;
    row < document.getElementById("roof-combination-table").rows.length;
    row++
  ) {
    for (
      let cell = 0;
      cell <
      document.getElementById("roof-combination-table").rows[row].cells.length;
      cell++
    ) {
      document
        .getElementById("roof-combination-table")
        .rows[row].cells[cell].classList.remove("skeleton-loader");
    }
  }

  document.getElementById("save-button").disabled = false;
}

/**
 * Get the roof load combinations
 */
function getRoofLoadCombinations() {
  window.api.invoke("get-connection-address").then((connectionAddress) => {
    window.api
      .invoke("get-token") // Retrieve the token
      .then((token) => {
        const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("Accept", "application/json");
        myHeaders.append("Authorization", `Bearer ${token}`);

        const raw = JSON.stringify({
          uls_roof_type: ULS_ROOF_SELECTION,
          sls_roof_type: SLS_ROOF_SELECTION,
        });

        const requestOptions = {
          method: "POST",
          headers: myHeaders,
          body: raw,
          redirect: "follow",
        };

        startRoofCombintaionLoading();

        fetch(`${connectionAddress}/get_roof_load_combinations`, requestOptions)
          .then((response) => response.json())
          .then((result) => {
            let data = JSON.parse(result);
            let headers = data["upwind"][0];
            let upwind_data = data["upwind"][1];
            let downwind_data = data["downwind"][1];
            let table = document.getElementById("roof-combination-table");
            table.innerHTML = "";
            let tableString = "";
            tableString += "<thead>";
            tableString += "<tr>";
            tableString += `<th>Slope</th>`;
            headers.forEach((header) => {
              tableString += `<th>${header}</th>`;
            });
            tableString += "<tr>";
            tableString += "</thead>";
            tableString += "<tbody>";

            tableString += "<tr>";
            let upwindValues = ["Upwind"].concat(upwind_data);
            upwindValues.forEach((value) => {
              tableString += `<td>${value}</td>`;
            });
            tableString += "</tr>";

            tableString += "<tr>";
            let downWindValues = ["Downwind"].concat(downwind_data);
            downWindValues.forEach((value) => {
              tableString += `<td>${value}</td>`;
            });
            tableString += "</tr>";

            tableString += "</tbody>";
            table.innerHTML = tableString;

            stopRoofCombinationLoading();
          })
          .catch((error) => {
            console.error(error);
            stopRoofCombinationLoading();
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
 * When the profile button is clicked, the user is redirected to the profile page.
 */
document.getElementById("profile").addEventListener("click", function () {
  window.location.href = "profile.html";
});

/**
 * When the logout button is clicked, the user is logged out and redirected to the login page.
 */
document.getElementById("logout").addEventListener("click", function () {
  window.api.invoke("store-token", "");
  window.location.href = "login.html";
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// VISUALIZATION
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function generate_bar_chart() {
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

        document.getElementById("bar-chart-render-error").style.display =
          "block";
        document.getElementById("bar-chart-render-error").innerHTML =
          "You have been placed in a rendering queue. Please wait for the render to complete...";

        fetch(`${connectionAddress}/bar_chart`, requestOptions)
          .then((response) => response.json())
          .then((result) => {
            let data = JSON.parse(result);
            let id = data["id"];
            let numBarCharts = data["num_bar_charts"];
            for (let i = 0; i < numBarCharts; i++) {
              // if i is even
              if (i % 3 === 0) {
                let img = document.createElement("img");
                setBarChartImage(connectionAddress, id, i, img, "left");
              } else if (i % 3 === 1) {
                let img = document.createElement("img");
                setBarChartImage(connectionAddress, id, i, img, "middle");
              } else {
                let img = document.createElement("img");
                setBarChartImage(connectionAddress, id, i, img, "right");
              }
            }

            document.getElementById("bar-chart-render-error").style.display =
              "none";
            document.getElementById("bar-chart-render-error").innerHTML = "";
          })
          .catch((error) => {
            console.error(error);
            document.getElementById("bar-chart-render-error").style.display =
              "block";
            document.getElementById("bar-chart-render-error").innerHTML =
              "Render failed. Please try again.";
          });
      });
  });
}

function generate_load_model() {
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

        document.getElementById("model-render-error").style.display = "block";
        document.getElementById("model-render-error").innerHTML =
          "You have been placed in a rendering queue. Please wait for the render to complete...";

        fetch(`${connectionAddress}/load_model`, requestOptions)
          .then((response) => response.json())
          .then((result) => {
            let id = JSON.parse(result);

            setWindLoadModelImage(connectionAddress, id);
            setSeismicLoadModelImage(connectionAddress, id);

            document.getElementById("model-render-error").style.display =
              "none";
            document.getElementById("model-render-error").innerHTML = "";
          })
          .catch((error) => {
            console.error(error);
            document.getElementById("model-render-error").style.display =
              "block";
            document.getElementById("model-render-error").innerHTML =
              "Render failed. Please try again.";
          });
      });
  });
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// WINDOW ONLOAD EVENT
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 * Set up the page on load
 */
window.onload = function () {
  setUsernameDropdown();
  loadSaveFile();

  const selectors = [
    "#uls-wall-selection",
    "#sls-wall-selection",
    "#uls-roof-selection",
    "#sls-roof-selection",
  ];

  selectors.forEach((selector) => toggleMenuColors(selector));

  // generate_load_model();
  // generate_bar_chart();
};
