document.getElementById('viewEntry').addEventListener('submit', updateentry);
// document.getElementById('deleteentryData').addEventListener('submit', deleteentry);
function updateentry(e) {
    e.preventDefault();
    let Token = localStorage.getItem('token');
    let id = sessionStorage.getItem('id');
    let url = 'http://127.0.0.1:5000/api/v1/entries/' + id;

    var newname = document.getElementById("nname").value;
    var newduedate = document.getElementById("nduedate").value;
    var newtype = document.getElementById("ntype").value;
    var newpurpose = document.getElementById("npurpose").value;

    fetch(url, {
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
        })
        .then(function (data) {
            if (data.Message === "modified your entry succesfully!") {
                alert("Message : " + data.Message);
                window.location.href = './viewdiaries.html';
            } else if (data.msg === "Token has expired") {
                // document.getElementById("result").innerHTML = "Message : " + data.msg;
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

function deleteentry(){
    // e.preventDefault();
    let Token = localStorage.getItem('token');
    let id = sessionStorage.getItem('id');
    let url = 'http://127.0.0.1:5000/api/v1/entries/' + id;

    fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${Token}`
        },
    })
        .then(function (response) {
            return response.json();
        })
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