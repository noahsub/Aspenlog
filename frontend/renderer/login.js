document.getElementById('signin').addEventListener('click', function(event) {
    event.preventDefault();
    // Your code here
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    var myHeaders = new Headers();
    myHeaders.append("Accept", "application/json");

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        redirect: 'follow'
    };

    fetch(`http://localhost:42613/login?username=${username}&password=${password}`, requestOptions)
        .then(response => {
            if (response.status === 401){
                throw new Error('Invalid Credentials');
            }
            return response.json();
        })
        .then(result => {
            const token = result.access_token;
            window.api.invoke('store-token', token);  // Store the token
            window.location.href = 'home.html';
        })
        .catch(error => {
            console.log('error', error);
            document.getElementById('error-message').textContent = error.message;
        });
});

document.getElementById('username').addEventListener('input', function(event){
    if (document.getElementById('error-message').textContent !== "")
    {
        document.getElementById('error-message').textContent = "";
    }
});

document.getElementById('password').addEventListener('input', function(event){
    if (document.getElementById('error-message').textContent !== "")
    {
        document.getElementById('error-message').textContent = "";
    }
});

document.getElementById('connection-details-button').addEventListener('click', function(event) {
    window.location.href = 'connection_details.html';
});

window.onload = function()
{
    var myHeaders = new Headers();
    myHeaders.append("Accept", "application/json");
    myHeaders.append('pragma', 'no-cache');
    myHeaders.append('cache-control', 'no-cache');

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
    };

    let serverStatus = document.getElementById('server-status');

    fetch("http://localhost:42613/server_status", requestOptions)
        .then(response => {

            if (response.status === 200)
            {
                serverStatus.innerHTML = 'Server Online ✓';
                serverStatus.style.color = '#9bca6d';
            }
            else
            {
                serverStatus.innerHTML = 'Server Offline ✕';
                serverStatus.style.color = '#9bca6d';
            }
        })
        .then(result => console.log(result))
        .catch(error => {
            serverStatus.innerHTML = 'Server Offline ✕';
            serverStatus.style.color = '#e64f4f';

            document.getElementById('username').disabled = true;
            document.getElementById('password').disabled = true;
            document.getElementById('signin').disabled = true;
            document.getElementById('join-button').style.visibility = 'hidden';
            document.getElementById('error-message').innerHTML = 'Server outage! Either switch to another server or wait for the current one to recover.';
        });
};