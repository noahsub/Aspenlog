////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// home.js
// This file contains the scripts for the home page.
//
// Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code
// By using this code, you agree to abide by the terms and conditions in those files.
//
// Author: Noah Subedar [https://github.com/noahsub]
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// GLOBALS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// The array to store the project IDs
let PROJECT_ARRAY = [];

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
 * When the user clicks the profile button they are redirected to the profile page
 */
document.getElementById("profile").addEventListener("click", function () {
  window.location.href = "profile.html";
});

/**
 * When the user clicks the logout button they are logged out and redirected to the login page
 */
document.getElementById("logout").addEventListener("click", function () {
  window.api.invoke("store-token", "");
  window.location.href = "login.html";
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// BUTTON CLICK EVENTS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Handles click events for the save file list, such as opening a save file, downloading a save file,
 * and removing a save file
 */
document
  .getElementById("save-file-list")
  .addEventListener("click", function (event) {
    // Download button was clicked
    if (event.target.matches(".download-button")) {
      let list_id = parseInt(event.target.closest(".list-group-item").id);
      let id = PROJECT_ARRAY[list_id];

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

            fetch(
              `${connectionAddress}/download_user_save_file?id=${id}`,
              requestOptions,
            )
              .then((response) => {
                // Get filename from Content-Disposition header
                const contentDisposition = response.headers.get(
                  "Content-Disposition",
                );
                let filename = "default_filename.extension";
                if (contentDisposition) {
                  const filenameRegex =
                    /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
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
              })
              .catch((error) => console.error(error));
          });
      });
    }
    // Remove button was clicked
    else if (event.target.matches(".remove-button")) {
      let list_id = parseInt(event.target.closest(".list-group-item").id);
      let id = PROJECT_ARRAY[list_id];

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

            fetch(
              `${connectionAddress}/delete_user_current_save_file?id=${id}`,
              requestOptions,
            )
              .then((response) => response.text())
              .then((result) => {
                let element = document.getElementById(list_id);
                element.parentNode.removeChild(element);
                PROJECT_ARRAY[list_id] = null;
              })
              .catch((error) => console.error(error));
          });
      });
    }
    // The parent div itself was clicked
    else if (event.target.matches(".list-group-item")) {
      let list_id = parseInt(event.target.id);
      let id = PROJECT_ARRAY[list_id];

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

            fetch(
              `${connectionAddress}/set_user_current_save_file?current_save_file=${id}`,
              requestOptions,
            )
              .then((response) => {
                if (response.status === 200) {
                  window.location.href = "input.html";
                } else {
                  throw new Error("Set User Current Save File Error");
                }
              })
              .catch((error) => console.error(error));
          });
      });
    }
  });

/**
 * Creates a new save file and redirects the user to the input page
 */
document.getElementById("new-button").addEventListener("click", function () {
  window.api.invoke("get-connection-address").then((connectionAddress) => {
    window.api
      .invoke("get-token") // Retrieve the token
      .then((token) => {
        const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("Accept", "application/json");
        myHeaders.append("Authorization", `Bearer ${token}`);

        const raw = JSON.stringify({
          json_data:
            '{"input_page":{"radio":{},"input":{"project-name":"New Project"},"table":{}}}',
          id: null,
        });

        const requestOptions = {
          method: "POST",
          headers: myHeaders,
          body: raw,
          redirect: "follow",
        };

        fetch(`${connectionAddress}/set_user_save_data`, requestOptions)
          .then((response) => {
            if (response.status === 200) {
              return response.json();
            } else {
              throw new Error("Set User Save Data Error");
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
              `${connectionAddress}/set_user_current_save_file?current_save_file=${id}`,
              requestOptions,
            )
              .then((response) => {
                if (response.status === 200) {
                  window.location.href = "input.html";
                } else {
                  throw new Error("Set User Current Save File Error");
                }
              })
              .catch((error) => console.error(error));
          })
          .catch((error) => console.error(error));
      });
  });
});

/**
 * Clicks the hidden file input element to open the file dialog
 */
document.getElementById("open-button").addEventListener("click", function () {
  document.getElementById("json-input").click();
});

/**
 * When a file is selected, the file is read and the data is sent to the server to create a new save file
 */
document.getElementById("json-input").addEventListener("change", function (e) {
  var file = e.target.files[0];
  var reader = new FileReader();

  reader.onload = function (e) {
    var content = e.target.result;

    window.api.invoke("get-connection-address").then((connectionAddress) => {
      window.api
        .invoke("get-token") // Retrieve the token
        .then((token) => {
          const myHeaders = new Headers();
          myHeaders.append("Content-Type", "application/json");
          myHeaders.append("Accept", "application/json");
          myHeaders.append("Authorization", `Bearer ${token}`);

          const raw = JSON.stringify({
            json_data: JSON.parse(content),
            id: null,
          });

          const requestOptions = {
            method: "POST",
            headers: myHeaders,
            body: raw,
            redirect: "follow",
          };

          fetch(`${connectionAddress}/set_user_save_data`, requestOptions)
            .then((response) => {
              if (response.status === 200) {
                return response.json();
              } else {
                throw new Error("Set User Save Data Error");
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
                `${connectionAddress}/set_user_current_save_file?current_save_file=${id}`,
                requestOptions,
              )
                .then((response) => {
                  if (response.status === 200) {
                    window.location.href = "input.html";
                  } else {
                    throw new Error("Set User Current Save File Error");
                  }
                })
                .catch((error) => console.error(error));
            })
            .catch((error) => console.error(error));
        });
    });
  };

  reader.readAsText(file);
});
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// WINDOW LOADED
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * When the window is loaded, the username dropdown is set and the save file list is populated
 */
window.onload = function () {
  setUsernameDropdown();

  PROJECT_ARRAY = [];

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

        fetch(`${connectionAddress}/get_all_user_save_data`, requestOptions)
          .then((response) => {
            if (response.status === 200) {
              return response.json();
            } else {
              throw new Error("Get All User Save Data Error");
            }
          })
          .then((data) => {
            if (Array.isArray(data)) {
              let list = document.getElementById("save-file-list");
              data.forEach((item, index) => {
                let data = JSON.parse(item.JsonData);
                let date = new Date(item.DateModified);
                let formattedDate =
                  date.toLocaleDateString() + " " + date.toLocaleTimeString();
                PROJECT_ARRAY.push(item.ID);

                // if there is a corrupted save file, skip it
                try {
                  const html = `
                            <div class="list-group-item d-flex justify-content-between align-items-center" id="${index}">
                                <div>
                                    <h4 class="list-group-item-heading">${data["input_page"]["input"]["project-name"]}</h4>
                                    <p class="list-group-item-text">${formattedDate}</p>
                                </div>
                                <div class="row">
                                    <div class="col">
                                        <button class="btn btn-primary download-button" style="width: 100%;">Download</button>
                                    </div>
                                    <div class="col">
                                        <button class="btn btn-primary remove-button" style="width: 100%;">Remove</button>
                                    </div>
                                </div>
                            </div>`;
                  list.innerHTML += html;
                } catch (err) {
                  console.error(err);
                }
              });
            } else {
              throw new Error("Get All User Save Data Error");
            }
          })
          .catch((error) => console.error(error));
      });
  });
};
