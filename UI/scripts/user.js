document.getElementById('register').addEventListener('submit', signup)
function signup(e) {
    e.preventDefault();
    var url = 'http://127.0.0.1:5000/api/v1/auth/signup';
    var Pusername = document.getElementById("username1").value;
    var Ppassword = document.getElementById("password1").value;
    // var password2 = document.getElementById('password2').value;
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
    .then(function(data){
        if (data.Message === "Created Succesfully"){
            document.getElementById("call").innerHTML = "Success :" + data.Message;
            window.location.href = "./index.html"
        } else {
            document.getElementById("call").innerHTML = "Fail :" + data.Message;
            }
    })
    .catch(function (error) {  
        console.log('Request failure: ', error);  
    });
}
function signin() {}