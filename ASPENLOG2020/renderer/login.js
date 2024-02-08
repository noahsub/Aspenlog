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
            window.api.sendToken(token);
            window.location.href = 'input.html';
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