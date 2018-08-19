document.getElementById('getentryData').addEventListener('submit', getentry);
function getentry(e) {
    e.preventDefault();
    var Token = localStorage.getItem('token');
    var id = sessionStorage.getItem('id');
    var url = 'http://127.0.0.1:5000/api/v1/entries/'+id;

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
            if (data.Message === "You dont have a specific entry with that *id*!") {
                document.getElementById("result").innerHTML = "Message : " + data.Message;
            } else if (data.entry != "") {
                var object = data.entry;
                var i = 0;
                var objectlength = object.length;
                for (i; i < objectlength; i++) {
                // var id = object[i].id;
                var name = object[i].name;
                var due_date = object[i].due_date;
                var type = object[i].type;
                var purpose = object[i].purpose;
                var date_created = object[i].date_created;

                oFormObject = document.forms['viewEntry'];
                oFormObject.elements["name"].value = name;
                oFormObject.elements["duedate"].value = due_date;
                oFormObject.elements["type"].value = type;
                oFormObject.elements["purpose"].value = purpose;
                oFormObject.elements["datecreated"].value = date_created;
                }
            } else {
                document.getElementById("result").innerHTML = "Message : " + data.Msg;
            };
        });
}