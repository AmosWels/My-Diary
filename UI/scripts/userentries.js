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
                document.getElementById("result").innerHTML = "Message : " + data.Message;
            } else if (data.entries != "") {
                var object = data.entries;
                var table = document.getElementsByTagName("table")[0];

                var objectlength = object.length;
                for (var i = 0; i < objectlength; i++) {
                    var id = object[i].id;
                    var name = object[i].name;
                    var due_date = object[i].due_date;
                    var type = object[i].type;
                    var purpose = object[i].purpose;
                    var date_created = object[i].date_created;

                    var newRow = table.insertRow(table.rows.length);
                    var cel1 = newRow.insertCell(0);
                    var cel2 = newRow.insertCell(1);
                    var cel3 = newRow.insertCell(2);
                    var cel4 = newRow.insertCell(3);
                    var cel5 = newRow.insertCell(4);
                    var cel6 = newRow.insertCell(5);

                    cel1.innerHTML = id;
                    cel2.innerHTML = name;
                    cel3.innerHTML = due_date;
                    cel4.innerHTML = type;
                    cel5.innerHTML = purpose;
                    cel6.innerHTML = date_created;
                }
            } else {
                document.getElementById("result").innerHTML = "Message : " + data.Msg;
            };
        });
}