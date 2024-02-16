function isAlphanumeric(str) {
    var regex = /^[a-z0-9]+$/i;
    return regex.test(str);
}

function isValidEmail(email) {
    var regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email);
}

var username_valid = false;
var password_valid = false;
var confirm_password_valid = false;

document.getElementById('username').addEventListener('input', function(event){
    // boolean array to check if all conditions are met
    var conditions = [false, false];
    // check if username is between 5 and 20 characters
    if (document.getElementById('username').value.length < 5 || document.getElementById('username').value.length > 20){
        // change color of text to red
        document.getElementById('username-length').style.color = "red";
        conditions[0] = false;
    }

    else{
        // change color of text to black
        document.getElementById('username-length').style.color = "black";
        conditions[0] = true;
    }

    // check if username is between 5 and 20 characters
    if (!isAlphanumeric(document.getElementById('username').value)){
        // change color of text to red
        document.getElementById('username-alphanumeric').style.color = "red";
        conditions[1] = false;
    }

    else{
        // change color of text to black
        document.getElementById('username-alphanumeric').style.color = "black";
        conditions[1] = true;
    }

    // if all conditions are met, set username_valid to true
    username_valid = conditions[0] && conditions[1];
});



document.getElementById('password').addEventListener('input', function(event){
    // boolean array to check if all conditions are met
    var conditions = [false, false, false, false, false];
    // check if password is between 8 and 20 characters
    if (document.getElementById('password').value.length < 10){
        // change color of text to red
        document.getElementById('password-length').style.color = "red";
        conditions[0] = false;
    }

    else{
        // change color of text to black
        document.getElementById('password-length').style.color = "black";
        conditions[0] = true;
    }

    // check if password contains at least one uppercase letter
    if (document.getElementById('password').value === document.getElementById('password').value.toLowerCase()){
        // change color of text to red
        document.getElementById('password-uppercase').style.color = "red";
        conditions[1] = false;
    }

    else{
        // change color of text to black
        document.getElementById('password-uppercase').style.color = "black";
        conditions[1] = true;
    }

    // check if password contains at least one lowercase letter
    if (document.getElementById('password').value === document.getElementById('password').value.toUpperCase()){
        // change color of text to red
        document.getElementById('password-lowercase').style.color = "red";
        conditions[2] = false;
    }

    else{
        // change color of text to black
        document.getElementById('password-lowercase').style.color = "black";
        conditions[2] = true;
    }

    // check if password contains at least one digit
    if (!/\d/.test(document.getElementById('password').value)){
        // change color of text to red
        document.getElementById('password-digit').style.color = "red";
        conditions[3] = false;
    }

    else{
        // change color of text to black
        document.getElementById('password-digit').style.color = "black";
        conditions[3] = true;
    }

    // check if password contains at least one special character
    if (document.getElementById('password').value.match(/[!@#$%^&*(),.?":{}|<>]/) === null){
        // change color of text to red
        document.getElementById('password-special').style.color = "red";
        conditions[4] = false;
    }

    else{
        // change color of text to black
        document.getElementById('password-special').style.color = "black";
        conditions[4] = true;
    }

    // if all conditions are met, set password_valid to true
    password_valid = conditions[0] && conditions[1] && conditions[2] && conditions[3] && conditions[4];
});

// check that the password and confirm password match
document.getElementById('confirm-password').addEventListener('input', function(event){
    if (document.getElementById('password').value !== document.getElementById('confirm-password').value)
    {
        document.getElementById('password-match').style.color = "red";
        confirm_password_valid = false;
    }

    else
    {
        document.getElementById('password-match').style.color = "black";
        confirm_password_valid = true;
    }
});

window.onload = function() {
    // disable the register button until all fields are valid
    document.getElementById('register').disabled = true;

    var inputs = document.getElementsByTagName('input');

    for (var i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('input', function() {
            // check if all fields are valid this includes first name, last name, and email
            first_name_valid = document.getElementById('firstname').value.length > 0;
            last_name_valid = document.getElementById('lastname').value.length > 0;
            email_valid = isValidEmail(document.getElementById('email').value)

            if (username_valid && password_valid && confirm_password_valid && first_name_valid && last_name_valid && email_valid)
            {
                // enable the register button
                document.getElementById('register').disabled = false;
            }

            else
            {
                // disable the register button
                document.getElementById('register').disabled = true;
            }
        });
    }
}

// register button click
document.getElementById('register').addEventListener('click', function(event) {
    event.preventDefault();

    var first_name = document.getElementById('firstname').value;
    var last_name = document.getElementById('lastname').value;
    var username = document.getElementById('username').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    var myHeaders = new Headers();
    myHeaders.append("Accept", "application/json");

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        redirect: 'follow'
    };

    fetch(`http://localhost:42613/register?username=${username}&first_name=${first_name}&last_name=${last_name}&password=${password}&email=${email}`, requestOptions)
        .then(response => response.json())
        .then(result => window.location.href = "login.html")
        .catch(error => console.log('error', error));
});

