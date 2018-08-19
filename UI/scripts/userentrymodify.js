document.getElementById('viewEntry').addEventListener('submit', updateentry);
function updateentry(e) {
    e.preventDefault();
    var Token = localStorage.getItem('token');
    var id = sessionStorage.getItem('id');
    var url = 'http://127.0.0.1:5000/api/v1/entries/'+id;

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
            } else {
                document.getElementById("call").innerHTML = "Fail : " + data.Message;
            }
        })
        .catch(function (error) {
            console.log('Request failure: ', error);
        });
}

