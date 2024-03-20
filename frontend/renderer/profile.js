////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// profile.js
// This file contains the scripts for the profile page.
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
 * When the home button is clicked, the user is redirected to the home page.
 */
document.getElementById("home-button").addEventListener("click", function ()
{
    window.location.href = "home.html";
});

/**
 * When the logout button is clicked, the user is logged out and redirected to the login page.
 */
document.getElementById("logout-button").addEventListener("click", function ()
{
    window.api.invoke("store-token", "");
    window.location.href = "login.html";
});

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// API CALLS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Retrieves the user's profile information from the backend and displays it on the page.
 */
function getProfile()
{
    window.api
        .invoke("get-connection-address").then((connectionAddress) =>
    {
        window.api
            .invoke("get-token") // Retrieve the token
            .then((token) =>
            {
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
                    .then((result) =>
                    {
                        let data = JSON.parse(result);
                        document.getElementById("first-name").innerHTML = data["first_name"];
                        document.getElementById("last-name").innerHTML = data["last_name"];
                        document.getElementById("username").innerHTML = data["username"];
                        document.getElementById("email").innerHTML = data["email"];
                    })
                    .catch((error) => window.location.href = "login.html");
            });
    });
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// WINDOW ONLOAD EVENT
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Set up the page on load
 */
window.onload = function ()
{
    getProfile();
};