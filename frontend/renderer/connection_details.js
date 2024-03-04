////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// BUTTON CLICK EVENTS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * When the connect button is clicked, the address and port are retrieved from the input fields and a request is made
 * to the server to check if the server is reachable.
 */
document
    .getElementById("connect-button")
    .addEventListener("click", function (event)
    {
        document.getElementById("address")
            .classList.add("skeleton-loader");
        document.getElementById("port")
            .classList.add("skeleton-loader");
        document.getElementById("https")
            .disabled = true;
        document.getElementById("connect-button")
            .classList.add("skeleton-loader");
        document.getElementById("login-button")
            .classList.add("skeleton-loader");

        var myHeaders = new Headers();
        myHeaders.append("Accept", "application/json");
        myHeaders.append("pragma", "no-cache");
        myHeaders.append("cache-control", "no-cache");

        var requestOptions = {
            method: "GET",
            headers: myHeaders,
            redirect: "follow",
        };

        let fullAddress;
        if (document.getElementById("https")
            .checked)
        {
            fullAddress =
                "https://" +
                document.getElementById("address")
                    .value +
                ":" +
                document.getElementById("port")
                    .value;
        }
        else
        {
            fullAddress =
                "http://" +
                document.getElementById("address")
                    .value +
                ":" +
                document.getElementById("port")
                    .value;
        }

        fetch(`${fullAddress}/server_status`, requestOptions)
            .then((response) =>
            {
                if (response.status === 200)
                {
                    window.api.invoke("store-connection-address", fullAddress); // Store the token
                    window.location.href = "login.html";
                }
                else
                {
                    let errorMessage = document.getElementById("error-message");
                    errorMessage.innerHTML = "Cannot Connect to Server";
                    errorMessage.style.color = "#e64f4f";

                    // Remove the skeleton loader
                    document
                        .getElementById("address")
                        .classList.remove("skeleton-loader");
                    document.getElementById("port")
                        .classList.remove("skeleton-loader");
                    document.getElementById("https")
                        .disabled = false;
                    document
                        .getElementById("connect-button")
                        .classList.remove("skeleton-loader");
                    document
                        .getElementById("login-button")
                        .classList.remove("skeleton-loader");
                }
            })
            .catch((error) =>
            {
                let errorMessage = document.getElementById("error-message");
                errorMessage.innerHTML = "Cannot Connect to Server";
                errorMessage.style.color = "#e64f4f";

                // Remove the skeleton loader
                document.getElementById("address")
                    .classList.remove("skeleton-loader");
                document.getElementById("port")
                    .classList.remove("skeleton-loader");
                document.getElementById("https")
                    .disabled = false;
                document
                    .getElementById("connect-button")
                    .classList.remove("skeleton-loader");
                document
                    .getElementById("login-button")
                    .classList.remove("skeleton-loader");
            });
    });

/**
 * When the login button is clicked, the user is redirected to the login page.
 */
document
    .getElementById("login-button")
    .addEventListener("click", function (event)
    {
        window.location.href = "login.html";
    });

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// WINDOW LOADED
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * When the window loads, the connection details are retrieved from the main process and the address and port
 * are set to the input fields.
 **/
window.onload = function ()
{
    window.api
        .invoke("get-connection-address") // Retrieve the token
        .then(async (connection) =>
        {
            // parse connection as a string
            connection = connection.toString();
            // extract the security type (https/http), address and port from the connection string
            const [security, address, port] = connection.split(":");
            // set address input value to the address
            document.getElementById("address")
                .value = address.substring(
                2,
                address.length,
            );
            // set port input value to the port
            document.getElementById("port")
                .value = port;

            // check the security type and set the checkbox accordingly
            if (security === "https")
            {
                document.getElementById("https")
                    .checked = true;
            }
        });
};