////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// register.js
// This file contains the scripts for the register page.
//
// Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code
// By using this code, you agree to abide by the terms and conditions in those files.
//
// Author: Noah Subedar [https://github.com/noahsub]
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// GLOBALS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

var USERNAME_VALID = false;
var PASSWORD_VALID = false;
var CONFIRM_PASSWORD_VALID = false;

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// HELPER FUNCTIONS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Check if a string is alphanumeric
 * @param str
 * @returns {boolean}
 */
function isAlphanumeric(str) {
  var regex = /^[a-z0-9]+$/i;
  return regex.test(str);
}

/**
 * Check if an email is valid
 * @param email
 * @returns {boolean}
 */
function isValidEmail(email) {
  var regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return regex.test(email);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// INPUT EVENTS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * When the username input is changed, check if the username is valid.
 */
document.getElementById("username").addEventListener("input", function (event) {
  // boolean array to check if all conditions are met
  var conditions = [false, false];
  // check if username is between 5 and 20 characters
  if (
    document.getElementById("username").value.length < 5 ||
    document.getElementById("username").value.length > 20
  ) {
    // change color of text to red
    document.getElementById("username-length").style.color = "red";
    conditions[0] = false;
  } else {
    // change color of text to black
    document.getElementById("username-length").style.color = "black";
    conditions[0] = true;
  }

  // check if username is between 5 and 20 characters
  if (!isAlphanumeric(document.getElementById("username").value)) {
    // change color of text to red
    document.getElementById("username-alphanumeric").style.color = "red";
    conditions[1] = false;
  } else {
    // change color of text to black
    document.getElementById("username-alphanumeric").style.color = "black";
    conditions[1] = true;
  }

  // if all conditions are met, set username_valid to true
  USERNAME_VALID = conditions[0] && conditions[1];
});

/**
 * When the password input is changed, check if the password is valid.
 */
document.getElementById("password").addEventListener("input", function (event) {
  // boolean array to check if all conditions are met
  var conditions = [false, false, false, false, false];
  // check if password is between 8 and 20 characters
  if (document.getElementById("password").value.length < 10) {
    // change color of text to red
    document.getElementById("password-length").style.color = "red";
    conditions[0] = false;
  } else {
    // change color of text to black
    document.getElementById("password-length").style.color = "black";
    conditions[0] = true;
  }

  // check if password contains at least one uppercase letter
  if (
    document.getElementById("password").value ===
    document.getElementById("password").value.toLowerCase()
  ) {
    // change color of text to red
    document.getElementById("password-uppercase").style.color = "red";
    conditions[1] = false;
  } else {
    // change color of text to black
    document.getElementById("password-uppercase").style.color = "black";
    conditions[1] = true;
  }

  // check if password contains at least one lowercase letter
  if (
    document.getElementById("password").value ===
    document.getElementById("password").value.toUpperCase()
  ) {
    // change color of text to red
    document.getElementById("password-lowercase").style.color = "red";
    conditions[2] = false;
  } else {
    // change color of text to black
    document.getElementById("password-lowercase").style.color = "black";
    conditions[2] = true;
  }

  // check if password contains at least one digit
  if (!/\d/.test(document.getElementById("password").value)) {
    // change color of text to red
    document.getElementById("password-digit").style.color = "red";
    conditions[3] = false;
  } else {
    // change color of text to black
    document.getElementById("password-digit").style.color = "black";
    conditions[3] = true;
  }

  // check if password contains at least one special character
  if (
    document
      .getElementById("password")
      .value.match(/[!@#$%^&*(),.?":{}|<>]/) === null
  ) {
    // change color of text to red
    document.getElementById("password-special").style.color = "red";
    conditions[4] = false;
  } else {
    // change color of text to black
    document.getElementById("password-special").style.color = "black";
    conditions[4] = true;
  }

  // if all conditions are met, set password_valid to true
  PASSWORD_VALID =
    conditions[0] &&
    conditions[1] &&
    conditions[2] &&
    conditions[3] &&
    conditions[4];
});

/**
 * When the confirm password input is changed, check if the password and confirm password match.
 */
document
  .getElementById("confirm-password")
  .addEventListener("input", function (event) {
    if (
      document.getElementById("password").value !==
      document.getElementById("confirm-password").value
    ) {
      document.getElementById("password-match").style.color = "red";
      CONFIRM_PASSWORD_VALID = false;
    } else {
      document.getElementById("password-match").style.color = "black";
      CONFIRM_PASSWORD_VALID = true;
    }
  });

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// BUTTON CLICK EVENTS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * When the register button is clicked, the user is redirected their credentials are stored in the backend and they
 * are redirected to the login page.
 */
document.getElementById("register").addEventListener("click", function (event) {
  event.preventDefault();

  window.api.invoke("get-connection-address").then((connectionAddress) => {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Accept", "application/json");

    let first_name = document.getElementById("firstname").value.toString();
    let last_name = document.getElementById("lastname").value.toString();
    let username = document.getElementById("username").value.toString();
    let email = document.getElementById("email").value.toString();
    let password = document.getElementById("password").value.toString();

    const raw = JSON.stringify({
      username: username,
      first_name: first_name,
      last_name: last_name,
      password: password,
      email: email,
    });

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: raw,
      redirect: "follow",
    };

    fetch(`${connectionAddress}/register`, requestOptions)
      .then((response) => response.json())
      .then((result) => {
        window.location.href = "login.html";
      })
      .catch((error) => console.error(error));
  });
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// WINDOW ONLOAD EVENT
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Set up the page on load
 */
window.onload = function () {
  // disable the register button until all fields are valid
  document.getElementById("register").disabled = true;

  var inputs = document.getElementsByTagName("input");

  for (var i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener("input", function () {
      // check if all fields are valid this includes first name, last name, and email
      first_name_valid = document.getElementById("firstname").value.length > 0;
      last_name_valid = document.getElementById("lastname").value.length > 0;
      email_valid = isValidEmail(document.getElementById("email").value);

      if (
        USERNAME_VALID &&
        PASSWORD_VALID &&
        CONFIRM_PASSWORD_VALID &&
        first_name_valid &&
        last_name_valid &&
        email_valid
      ) {
        // enable the register button
        document.getElementById("register").disabled = false;
      } else {
        // disable the register button
        document.getElementById("register").disabled = true;
      }
    });
  }
};
