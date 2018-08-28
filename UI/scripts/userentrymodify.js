document.getElementById('viewEntry').addEventListener('submit', updateentry);
function updateentry(e) {
    e.preventDefault();
    let Token = localStorage.getItem('token');
    let id = sessionStorage.getItem('id');
    let url = baseurl + '/api/v1/entries/' + id;
    var { newduedate, newname, newpurpose, newtype } = getupdateinput();
    fetchupdate(url, Token, newduedate, newname, newpurpose, newtype)
        .then(function (data) {
            if (data.Message === "modified your entry succesfully!") {
                alert("Message : " + data.Message);
                window.location.href = './viewdiaries.html';
            } else if (data.msg === "Token has expired") {
                alert("Message : " + data.msg + "\n Please Login again");
                window.location.href = './index.html';
            } else {
                document.getElementById("call").innerHTML = "Fail : " + data.Message;
            }
        })
        .catch(function (error) {
            console.log('Request failure: ', error)
        });
}

function getupdateinput() {
    var newname = document.getElementById("nname").value;
    var newduedate = document.getElementById("nduedate").value;
    var newtype = document.getElementById("ntype").value;
    var newpurpose = document.getElementById("npurpose").value;
    return { newduedate, newname, newpurpose, newtype };
}

function fetchupdate(url, Token, newduedate, newname, newpurpose, newtype) {
    return fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${Token}`
        },
        body: JSON.stringify({
            due_date: newduedate, name: newname, purpose: newpurpose, type: newtype
        })
    })
        .then(function (response) {
            return response.json();
        });
}

function deleteentry(){
    let Token = localStorage.getItem('token');
    let id = sessionStorage.getItem('id');
    let url = baseurl + '/api/v1/entries/' + id;

    fetchdelete(url, Token)
        .then(function (data) {
            if (data.Message === "Deleted your entry succesfully!") {
                window.location.href = './viewdiaries.html';
            } else if (data.msg === "Token has expired") {
                alert("Message : " + data.msg + "\n Please Login again");
                window.location.href = './index.html';
            } else {
                document.getElementById("call").innerHTML = "Fail : " + data.Message;
            }
        })
        .catch(function (error) {
            console.log('Request failure: ', error)
        });
}

function fetchdelete(url, Token) {
    return fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${Token}`
        },
    })
        .then(function (response) {
            return response.json();
        });
}
