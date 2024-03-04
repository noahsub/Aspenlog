let project_array = [];

function setUsernameDropdown()
{
    window.api.invoke('get-token') // Retrieve the token
        .then((token) =>{
            const myHeaders = new Headers();
            myHeaders.append("Accept", "application/json");
            myHeaders.append("Authorization", `Bearer ${token}`);

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                redirect: "follow"
            };

            fetch("http://localhost:42613/get_user_profile", requestOptions)
                .then((response) => response.json())
                .then((result) =>
                {
                    let data = JSON.parse(result);
                    username = data['username'];
                    document.getElementById('navbarDropdownMenuLink').textContent = username;
                })
                .catch((error) => console.error(error));
        });
}

window.onload = function()
{
    window.api.invoke('get-connection-address') // Retrieve the token
        .then((connectionAddress) =>{
            console.log(connectionAddress);
        });

    setUsernameDropdown();

    project_array = [];
    window.api.invoke('get-token') // Retrieve the token
        .then((token) =>
        {
            const myHeaders = new Headers();
            myHeaders.append("Accept", "application/json");
            myHeaders.append("Authorization", `Bearer ${token}`);

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                redirect: "follow"
            };

            fetch("http://localhost:42613/get_all_user_save_data", requestOptions)
                .then((response) =>
                {
                    if (response.status === 200)
                    {
                        return response.json();
                    }
                    else
                    {
                        throw new Error("Get All User Save Data Error");
                    }
                })
                .then((data) =>
                {
                    if (Array.isArray(data))
                    {
                        let list = document.getElementById("save-file-list");
                        data.forEach((item, index) =>
                        {
                            let data = JSON.parse(item.JsonData);
                            let date = new Date(item.DateModified);
                            let formattedDate = date.toLocaleDateString() + " " + date.toLocaleTimeString();
                            project_array.push(item.ID);

                            const html = `
                            <div class="list-group-item d-flex justify-content-between align-items-center" id="${index}">
                                <div>
                                    <h4 class="list-group-item-heading">${data['input_page']['input']['project-name']}</h4>
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
                        });
                    }
                    else
                    {
                        throw new Error("Get All User Save Data Error");
                    }
                })
                .catch((error) => console.error(error));
        });
};

// profile click event
document.getElementById("profile").addEventListener("click", function()
{
    window.location.href = 'profile.html';
});

// logout click event
document.getElementById("logout").addEventListener("click", function()
{
    window.api.invoke('store-token', '');
    window.location.href = 'login.html';
});

// Add event listener to the parent div
document.getElementById("save-file-list").addEventListener('click', function(event)
{
    // Download button was clicked
    if (event.target.matches('.download-button'))
    {
        let list_id = parseInt(event.target.closest('.list-group-item').id)
        let id = project_array[list_id]
        alert("This function is not yet implemented, please try again later.");
    }
    // Remove button was clicked
    else if (event.target.matches('.remove-button'))
    {
        let list_id = parseInt(event.target.closest('.list-group-item').id)
        let id = project_array[list_id]
        alert("This function is not yet implemented, please try again later.");
    }
    // The parent div itself was clicked
    else if (event.target.matches('.list-group-item'))
    {
        let list_id = parseInt(event.target.id)
        let id = project_array[list_id]
        window.api.invoke('get-token') // Retrieve the token
            .then((token) =>{
                const myHeaders = new Headers();
                myHeaders.append("Accept", "application/json");
                myHeaders.append("Authorization", `Bearer ${token}`);

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    redirect: "follow"
                };

                fetch(`http://localhost:42613/set_user_current_save_file?current_save_file=${id}`, requestOptions)
                    .then((response) =>
                    {
                        if (response.status === 200)
                        {
                            window.location.href = 'input.html';
                        }
                        else
                        {
                            throw new Error("Set User Current Save File Error");
                        }
                    })
                    .catch((error) => console.error(error));
            });

    }
});

// new-button click event
document.getElementById("new-button").addEventListener("click", function()
{
    window.api.invoke('get-token') // Retrieve the token
        .then((token) =>
        {
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Accept", "application/json");
            myHeaders.append("Authorization", `Bearer ${token}`);

            const raw = JSON.stringify(
                {
                    "json_data": "{\"input_page\":{\"radio\":{},\"input\":{\"project-name\":\"New Project\"},\"table\":{}}}",
                    "id": null
                });

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };

            fetch("http://localhost:42613/set_user_save_data", requestOptions)
                .then((response) =>
                {
                    if (response.status === 200)
                    {
                        return response.json();
                    }

                    else
                    {
                        throw new Error("Set User Save Data Error");
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
                        redirect: "follow"
                    };

                    fetch(`http://localhost:42613/set_user_current_save_file?current_save_file=${id}`, requestOptions)
                        .then((response) =>
                        {
                            if (response.status === 200)
                            {
                                window.location.href = 'input.html';
                            }
                            else
                            {
                                throw new Error("Set User Current Save File Error");
                            }
                        })
                        .catch((error) => console.error(error));
                })
                .catch((error) => console.error(error));
        });
});