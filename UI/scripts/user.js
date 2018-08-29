document.getElementById('register').addEventListener('submit', signup);
function signup(e) {
    e.preventDefault();
    let url = baseurl + '/api/v1/auth/signup';
    let { Ppassword, Ppassword2, Pusername } = getuserinput();
    if (Ppassword == Ppassword2){
        fetchuserdata(url, Pusername, Ppassword)
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
    } else {
        document.getElementById("call").innerHTML = "Fail : Your passwords Don't match";
    }
}

function getuserinput() {
    let Pusername = document.getElementById("username1").value;
    let Ppassword = document.getElementById("password1").value;
    let Ppassword2 = document.getElementById("password2").value;
    return { Ppassword, Ppassword2, Pusername };
}

function fetchuserdata(url, Pusername, Ppassword) {
    return fetch(url, {
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
        });
}
