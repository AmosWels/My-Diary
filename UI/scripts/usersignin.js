document.getElementById('userlogin').addEventListener('submit', login);
function login(e) {
    e.preventDefault();
    let url = baseurl + '/api/v1/auth/login';
    let { Pusername, Ppassword } = getlogininput();
    fetchuserlogin(url, Pusername, Ppassword)
    .then(function (data) {
        if (data.Message === "welcome, you have succesfully logged in !!!") {
            window.location.href = './viewdiaries.html';
            localStorage.setItem('token', data.token);
        } else {
            document.getElementById("call").innerHTML = "Fail : " + data.Message;
        }
    })
    .catch(function (error) {
        console.log('Request failure: ', error);
    });
}

function getlogininput() {
    let Pusername = document.getElementById("uname").value;
    let Ppassword = document.getElementById("upassword").value;
    return { Pusername, Ppassword };
}

function fetchuserlogin(url, Pusername, Ppassword) {
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
