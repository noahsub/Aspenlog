document.getElementById("home-button").addEventListener("click", function ()
{
    window.location.href = "home.html";
});

document.getElementById("logout-button").addEventListener("click", function ()
{
    window.api.invoke("store-token", "");
    window.location.href = "login.html";
});

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
                    .catch((error) => console.error(error));
            });
    });
}

window.onload = function ()
{
    getProfile();
};