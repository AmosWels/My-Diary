document.getElementById("createEntry").addEventListener("submit", create);
function create(e) {
    e.preventDefault();
    var Token = localStorage.getItem('token');
    var url = 'http://127.0.0.1:5000/api/v1/entries';

    var ename = document.getElementById("ename").value;
    var eduedate = document.getElementById("eduedate").value;
    var etype = document.getElementById("etype").value;
    var epurpose = document.getElementById("epurpose").value;
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'Authorization': `Bearer ${Token}`
        },
        body: JSON.stringify({
            due_date: eduedate, name: ename, purpose: epurpose, type: etype
        })
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.Message === "your entry has been succesfully created!") {
                // sessionStorage.setItem('token', data.token);
                alert("Message : "+ data.Message);
                document.getElementById("call").innerHTML = "Success :" + data.Message;
                window.location.href = './viewdiaries.html';
            } else {
                document.getElementById("call").innerHTML = "Fail : " + data.Message;
            }
        })
        .catch(function (error) {
            console.log('Request failure: ', error);
        });
}