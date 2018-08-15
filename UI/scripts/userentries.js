document.getElementById('getData').addEventListener('submit', getentries);
function getentries(e) {
    e.preventDefault();
    var Token = sessionStorage.getItem('token');
    var url = 'http://127.0.0.1:5000/api/v1/entries';
    
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${Token}`
        }
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.Message === "You haven't created any entries yet. Please create first.") {
                document.getElementById('result').innerHTML = "Success :" + data.Message;
            }
            if (data.entries != "") {
                var object = data.entries;
                var objectlength = object.length;
                var table = document.getElementById("customers");
                for (var i = 0; i < objectlength; i++) {
                    var record = document.createElement("tr");
                    var name = object[i].name;
                    var due_date = object[i].due_date;
                    var type = object[i].type;
                    var purpose = object[i].purpose;
                    var date_created = object[i].date_created;

                    document.getElementById("name").innerHTML = name;
                    document.getElementById("datecreated").innerHTML = date_created;
                    document.getElementById("type").innerHTML = type;
                    document.getElementById("purpose").innerHTML = purpose;
                    document.getElementById("duedate").innerHTML = due_date;
                }
            };
        });
}