window.onload = function()
{
    window.api.invoke('get-connection-address') // Retrieve the token
        .then(async (connection) => {
            const [_, address, port] = connection.address.split(":");
            document.getElementById('address').value = address;
            document.getElementById('port').value = port;

            document.getElementById('address').value = address;
            document.getElementById('port').value = port;
        });
};

document.getElementById('connect-button').addEventListener('click', function(event) {

});

document.getElementById('login-button').addEventListener('click', function(event) {
    window.location.href = 'login.html';
});