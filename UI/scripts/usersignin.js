document.getElementById('userlogin').addEventListener('submit', login);
function login(e) {
    e.preventDefault();
    var url = 'http://127.0.0.1:5000/api/v1/auth/login';
    var Pusername = document.getElementById("uname").value;
    var Ppassword = document.getElementById("upassword").value;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({
            username: Pusername, password: Ppassword
        })
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        if (data.Message === "welcome, you have succesfully logged in !!!") {
            window.location.href = './viewdiaries.html';
            localStorage.setItem('token', data.token);
            alert("Message : "+ data.Message);
        } else {
            document.getElementById("call").innerHTML = "Fail : " + data.Message;
        }
    })
    .catch(function (error) {
        console.log('Request failure: ', error);
    });
}