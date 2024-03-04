let ulsWallSelection;
let slsWallSelection;
let ulsRoofSelection;
let slsRoofSelection;

function toggleMenuColors(toggleMenu)
{
    document.querySelectorAll(toggleMenu + " .btn").forEach((button) =>
    {
        button.addEventListener("click", (event) =>
        {
            document.querySelectorAll(toggleMenu + " .btn").forEach((btn) =>
            {
                btn.classList.remove("selected");
            });
            event.currentTarget.classList.add("selected");
        });
    });
}

function waitForElement(id, callback)
{
    let intervalId = setInterval(function ()
    {
        let element = document.getElementById(id);
        if (element)
        {
            clearInterval(intervalId);
            callback(element);
        }
    }, 100); // Check every 100ms
}

function loadSaveFile()
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

                fetch(`${connectionAddress}/get_user_current_save_file`, requestOptions)
                    .then((response) =>
                    {
                        if (response.status === 200)
                        {
                            return response.json();
                        }
                        else
                        {
                            throw new Error("Get User Current Save File Error");
                        }
                    })
                    .then((result) =>
                    {
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
                            .then((response) =>
                            {
                                if (response.status === 200)
                                {
                                    return response.json();
                                }
                                else
                                {
                                    throw new Error("Get User Save File Error");
                                }
                            })
                            .then((data) =>
                            {
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
                                    .then((response) =>
                                    {
                                        if (response.status === 200)
                                        {
                                            return response.json();
                                        }
                                        else
                                        {
                                            throw new Error("Get User Save File Error");
                                        }
                                    })
                                    .then((result) =>
                                    {
                                        deserialize(result.JsonData, "result_page").then(() =>
                                        {
                                            window.scrollTo(0, 0);
                                        });
                                    })
                                    .catch((error) => console.error(error));
                            })
                            .catch((error) => console.error(error));
                    })
                    .catch((error) => console.error(error));
            });
    });

}

function serialize()
{
    let objects = {
        result_page:
            {
                radio:
                    {},
                input:
                    {},
            },
    };

    // Handle radio inputs
    let radios = document.querySelectorAll("input[type=radio]");
    radios.forEach((radio) =>
    {
        if (radio.checked)
        {
            objects.result_page.radio[radio.id] = radio.value;
        }
    });

    let json = JSON.stringify(objects);
    return json;
}

function deserialize(json, section)
{
    return new Promise((resolve) =>
    {
        let objects = JSON.parse(json)[section];
        let totalElements =
            Object.keys(objects.radio).length + Object.keys(objects.input).length;
        let processedElements = 0;

        // go through all the radio
        for (let id in objects.radio)
        {
            waitForElement(id, function (radio)
            {
                if (radio.value === objects.radio[id])
                {
                    radio.click();
                }
                processedElements++;
                if (processedElements === totalElements)
                {
                    resolve();
                }
            });
        }
    });
}

document.getElementById("save-button").addEventListener("click", () =>
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

                fetch(`${connectionAddress}/get_user_current_save_file`, requestOptions)
                    .then((response) =>
                    {
                        if (response.status === 200)
                        {
                            return response.json();
                        }
                        else
                        {
                            throw new Error("Get User Current Save File Error");
                        }
                    })
                    .then((result) =>
                    {
                        let id = parseInt(result);
                        const myHeaders = new Headers();
                        myHeaders.append("Content-Type", "application/json");
                        myHeaders.append("Accept", "application/json");
                        myHeaders.append("Authorization", `Bearer ${token}`);

                        const raw = JSON.stringify(
                            {
                                json_data: serialize(),
                                id: id,
                            });

                        const requestOptions = {
                            method: "POST",
                            headers: myHeaders,
                            body: raw,
                            redirect: "follow",
                        };

                        fetch(`${connectionAddress}/set_user_save_data`, requestOptions)
                            .then((response) => response.text())
                            .catch((error) => console.error(error));
                    })
                    .catch((error) => console.error(error));
            });
    });

});

document
    .getElementById("uls-wall-selection")
    .addEventListener("change", function (e)
    {
        let selectedOption = e.target.id;
        switch (selectedOption)
        {
            case "uls-wall-selection-dead-only-1-4D-option":
                ulsWallSelection = "uls_1.4D";
                break;
            case "uls-wall-selection-full-wind-1-25D-1-4Wy-option":
                ulsWallSelection = "uls_1.25D_1.4Wy";
                break;
            case "uls-wall-selection-seismic-1-0D-1-0Ey-option":
                ulsWallSelection = "uls_1.0D_1.0Ey";
                break;
            case "uls-wall-selection-seismic-1-0D-1-0Ex-option":
                ulsWallSelection = "uls_1.0D_1.0Ex";
                break;
        }

        if (ulsWallSelection !== undefined && slsWallSelection !== undefined)
        {
            getWallLoadCombinations();
        }
    });

// back button
document.getElementById("back-button").addEventListener("click", () =>
{
    window.location.href = "load.html";
});

document
    .getElementById("sls-wall-selection")
    .addEventListener("change", function (e)
    {
        let selectedOption = e.target.id;
        switch (selectedOption)
        {
            case "sls-wall-selection-1-0D-1-0Wy-option":
                slsWallSelection = "sls_1.0D_1.0Wy";
                break;
        }

        if (ulsWallSelection !== undefined && slsWallSelection !== undefined)
        {
            getWallLoadCombinations();
        }
    });

document
    .getElementById("uls-roof-selection")
    .addEventListener("change", function (e)
    {
        let selectedOption = e.target.id;
        switch (selectedOption)
        {
            case "uls-roof-selection-dead-only-1-4D-option":
                ulsRoofSelection = "uls_1.4D";
                break;
            case "uls-roof-selection-full-wind-1-25D-1-4Wy-option":
                ulsRoofSelection = "uls_1.25D_1.4Wy";
                break;
            case "uls-roof-selection-seismic-1-0D-1-0Ey-option":
                ulsRoofSelection = "uls_1.0D_1.0Ey";
                break;
            case "uls-roof-selection-seismic-1-0D-1-0Ex-option":
                ulsRoofSelection = "uls_1.0D_1.0Ex";
                break;
            case "uls-roof-selection-full-snow-with-wind-1-25D-1-5S-option":
                ulsRoofSelection = "uls_1.25D_1.5S";
                break;
        }

        if (ulsRoofSelection !== undefined && slsRoofSelection !== undefined)
        {
            getRoofLoadCombinations();
        }
    });

document
    .getElementById("sls-roof-selection")
    .addEventListener("change", function (e)
    {
        let selectedOption = e.target.id;
        switch (selectedOption)
        {
            case "sls-roof-selection-dead-and-wind-y-normal-to-face-1-0D-1-0Wy-option":
                slsRoofSelection = "sls_1.0D_1.0Wy";
                break;
            case "sls-roof-selection-full-snow-with-wind-y-1-0D-1-0S-option":
                slsRoofSelection = "sls_1.0D_1.0S";
                break;
            case "sls-roof-selection-dead-and-live-1-0D-1-0L-option":
                slsRoofSelection = "sls_1.0D_1.0L_WY";
                break;
        }

        if (ulsRoofSelection !== undefined && slsRoofSelection !== undefined)
        {
            getRoofLoadCombinations();
        }
    });

function getWallLoadCombinations()
{
    window.api
        .invoke("get-connection-address").then((connectionAddress) =>
    {
        window.api
            .invoke("get-token") // Retrieve the token
            .then((token) =>
            {
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Accept", "application/json");
                myHeaders.append("Authorization", `Bearer ${token}`);

                const raw = JSON.stringify(
                    {
                        uls_wall_type: ulsWallSelection,
                        sls_wall_type: slsWallSelection,
                    });

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow",
                };

                fetch(`${connectionAddress}/get_wall_load_combinations`, requestOptions)
                    .then((response) => response.text())
                    .then((result) =>
                    {
                        let data = JSON.parse(result);
                        let table = document.getElementById("wall-combination-table");
                        table.innerHTML = "";
                        let tableString = "";
                        tableString += "<thead>";
                        tableString += "<tr>";
                        let headers = Object.keys(data[0]);
                        tableString += `<th>Height Zone</th>`;
                        headers.forEach((header) =>
                        {
                            tableString += `<th>${header}</th>`;
                        });
                        tableString += "<tr>";
                        tableString += "</thead>";
                        tableString += "<tbody>";
                        for (let i = 0; i < data.length; i++)
                        {
                            tableString += "<tr>";
                            let values = Object.values(data[i]);
                            let newValues = [i + 1].concat(values);
                            newValues.forEach((value) =>
                            {
                                tableString += `<td>${value}</td>`;
                            });
                            tableString += "</tr>";
                        }
                        tableString += "</tbody>";
                        table.innerHTML = tableString;
                    })
                    .catch((error) => console.error(error));
            });

    });


}

function getRoofLoadCombinations()
{
    window.api
        .invoke("get-connection-address").then((connectionAddress) =>
    {
        window.api
            .invoke("get-token") // Retrieve the token
            .then((token) =>
            {
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Accept", "application/json");
                myHeaders.append("Authorization", `Bearer ${token}`);

                const raw = JSON.stringify(
                    {
                        uls_roof_type: ulsRoofSelection,
                        sls_roof_type: slsRoofSelection,
                    });

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow",
                };

                fetch(`${connectionAddress}/get_roof_load_combinations`, requestOptions)
                    .then((response) => response.json())
                    .then((result) =>
                    {
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
                        headers.forEach((header) =>
                        {
                            tableString += `<th>${header}</th>`;
                        });
                        tableString += "<tr>";
                        tableString += "</thead>";
                        tableString += "<tbody>";

                        tableString += "<tr>";
                        let upwindValues = ["Upwind"].concat(upwind_data);
                        upwindValues.forEach((value) =>
                        {
                            tableString += `<td>${value}</td>`;
                        });
                        tableString += "</tr>";

                        tableString += "<tr>";
                        let downWindValues = ["Downwind"].concat(downwind_data);
                        downWindValues.forEach((value) =>
                        {
                            tableString += `<td>${value}</td>`;
                        });
                        tableString += "</tr>";

                        tableString += "</tbody>";
                        table.innerHTML = tableString;
                    })
                    .catch((error) => console.error(error));
            });
    });
}

document.getElementById("home-button").addEventListener("click", function ()
{
    window.location.href = "home.html";
});

// profile click event
document.getElementById("profile").addEventListener("click", function ()
{
    window.location.href = "profile.html";
});

// logout click event
document.getElementById("logout").addEventListener("click", function ()
{
    window.api.invoke("store-token", "");
    window.location.href = "login.html";
});

function setUsernameDropdown()
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
                        username = data["username"];
                        document.getElementById("navbarDropdownMenuLink").textContent =
                            username;
                    })
                    .catch((error) => console.error(error));
            });
    });
}

window.onload = function ()
{
    setUsernameDropdown();
    loadSaveFile();

    const selectors = [
        "#uls-wall-selection",
        "#sls-wall-selection",
        "#uls-roof-selection",
        "#sls-roof-selection",
    ];

    selectors.forEach((selector) => toggleMenuColors(selector));
};