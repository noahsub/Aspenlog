////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// login.js
// This file contains the scripts for the login page.
//
// Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code
// By using this code, you agree to abide by the terms and conditions in those files.
//
// Author: Noah Subedar [https://github.com/noahsub]
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// BUTTON CLICK EVENTS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * When the signin button is clicked, the username and password are retrieved from the input fields and a request is made
 * to the backend to check if the credentials are valid. If they are, the user is redirected to the home page.
 */
document.getElementById("signin").addEventListener("click", function (event) {
  event.preventDefault();

  window.api.invoke("get-connection-address").then((connectionAddress) => {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Accept", "application/json");

    let username = document.getElementById("username").value.toString();
    let password = document.getElementById("password").value.toString();

    console.log(username);
    console.log(password);

    const raw = JSON.stringify({
      username: username,
      password: password,
    });

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: raw,
      redirect: "follow",
    };

    fetch(`${connectionAddress}/login`, requestOptions)
      .then((response) => {
        if (response.status !== 200) {
          throw new Error("Invalid Credentials");
        }

        return response.json();
      })
      .then((result) => {
        const token = result.access_token;
        window.api.invoke("store-token", token); // Store the token
        window.location.href = "home.html";
      })
      .catch(
        (error) =>
          (document.getElementById("error-message").textContent =
            "Invalid Credentials"),
      );
  });
});

/**
 * When the connection details button is clicked, the user is redirected to the connection details page.
 */
document
  .getElementById("connection-details-button")
  .addEventListener("click", function (event) {
    window.location.href = "connection_details.html";
  });

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// INPUT EVENTS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * If the user is typing and there is an error message, the error message is cleared.
 */
document.getElementById("username").addEventListener("input", function (event) {
  if (document.getElementById("error-message").textContent !== "") {
    document.getElementById("error-message").textContent = "";
  }
});

/**
 * If the user is typing and there is an error message, the error message is cleared.
 */
document.getElementById("password").addEventListener("input", function (event) {
  if (document.getElementById("error-message").textContent !== "") {
    document.getElementById("error-message").textContent = "";
  }
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// WINDOW ONLOAD EVENT
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

const delay = (ms) => new Promise((res) => setTimeout(res, ms));

function checkServer() {
  window.api.invoke("get-connection-address").then((connectionAddress) => {
    var myHeaders = new Headers();
    myHeaders.append("Accept", "application/json");
    myHeaders.append("pragma", "no-cache");
    myHeaders.append("cache-control", "no-cache");

    var requestOptions = {
      method: "GET",
      headers: myHeaders,
      redirect: "follow",
    };

    let serverStatus = document.getElementById("server-status");

    fetch(`${connectionAddress}/server_status`, requestOptions)
      .then(async (response) => {
        if (response.status === 200) {
          document.getElementById("username").disabled = false;
          document.getElementById("password").disabled = false;
          document.getElementById("signin").disabled = false;
          document.getElementById("join-button").style.visibility = "visible";
          document.getElementById("error-message").innerHTML = "";

          serverStatus.innerHTML = "Server Online ✓";
          serverStatus.style.color = "#9bca6d";

          await delay(5000);
          checkServer();
        } else {
          serverStatus.innerHTML = "Server Offline ✕";
          serverStatus.style.color = "#e64f4f";

          document.getElementById("username").disabled = true;
          document.getElementById("password").disabled = true;
          document.getElementById("signin").disabled = true;
          document.getElementById("join-button").style.visibility = "hidden";
          document.getElementById("error-message").innerHTML =
            "Server outage! Either switch to another server or wait for the current one to recover.";

          await delay(5000);
          checkServer();
        }
      })
      .catch(async (error) => {
        serverStatus.innerHTML = "Server Offline ✕";
        serverStatus.style.color = "#e64f4f";

        document.getElementById("username").disabled = true;
        document.getElementById("password").disabled = true;
        document.getElementById("signin").disabled = true;
        document.getElementById("join-button").style.visibility = "hidden";
        document.getElementById("error-message").innerHTML =
          "Server outage! Either switch to another server or wait for the current one to recover.";

        await delay(5000);
        checkServer();
      });
  });
}

/**
 * Set up the page on load
 */
window.onload = function () {
  checkServer();
};
