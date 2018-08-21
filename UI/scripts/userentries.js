document.getElementById('getData').addEventListener('submit', getentries);

function getentries(e) {
    e.preventDefault();
    var Token = localStorage.getItem('token');
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
                // sessionStorage.setItem('token', data.token);
            } else if (data.entries != "") {
                // sessionStorage.setItem('token', data.token);
                var object = data.entries;
                var table = document.getElementsByTagName("table")[0];
                var i = 0;
                var j = 1;
                var objectlength = object.length;
                for (i, j; i < objectlength, j <= objectlength; i++ , j++) {
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
                    var cel7 = newRow.insertCell(6);
                    var cel8 = newRow.insertCell(7);

                    cel1.innerHTML = j + '.';
                    cel2.innerHTML = '[ '+id+' ]';
                    cel3.innerHTML = name;
                    cel4.innerHTML = due_date;
                    cel5.innerHTML = type;
                    cel6.innerHTML = purpose;
                    cel7.innerHTML = date_created;
                    // cel7.innerHTML = window.location.href = './modifydiary.html';
                    cel8.innerHTML = "<a href='./modifydiary.html'>Actions</a>"
                    // sessionStorage.setItem('id', id);
                    // alert(id);
                    
                    // localStorage.setItem('ent_id',id)
                    // newRow.onclick(DoNav("./viewdiarycontent.html"))
                    // for (var k = 0; k < objectlength; k++) {
                    //     newRow[k].onclick =  alert(id);
                    //         // Do more stuff with this id.
                    // }
                }

                    


            } else {
                document.getElementById("result").innerHTML = "Message : " + data.Msg;
            };
        });
}

function getrow() {
    var table1 = document.getElementById("customers");
    var rows = table1.rows;
    var length = rows.length;
    for (var k = 0; k < length; k++) {
        rows[k].onclick =  alert(k);
            // Do more stuff with this id.
    }
}
// jQuery:
// $("#table-one tr").bind("click", function() {
//     alert(this.id);
// });
// function DoNav(theUrl) {
//     window.location.href = theUrl;
// }
// function getoneEntry(entryid) {
//     document.getElementById("modify").value;
//     var Token = localStorage.getItem('token');
//     var url = '/api/v1/entries/' + entryid;

//     fetch(url, {
//         method: 'GET',
//         headers: {
//             'Content-Type': 'application/json',
//             'Authorization': `Bearer ${Token}`
//         }
//     })
//         .then(function (response) {
//             return response.json();
//         })
//         .then(function (data) {
//             if (data.Message !="You dont have a specific entry with that *id*!") {
//                 document.getElementById("call").innerHTML = "Fail : " + data.Message;
//             } else if (data.entry != "") {
//                 // var id = object[i].id;
//                 // var name = object[i].name;
//                 // var due_date = object[i].due_date;
//                 // var type = object[i].type;
//                 // var purpose = object[i].purpose;
//                 // var date_created = object[i].date_created;
//                 // modal.style.display = 'block';
//                 document.getElementById('mname').innerHTML = name;
//                 document.getElementById('mduedate').innerHTML = due_date;
//                 document.getElementById('mtype').innerHTML = type;
//                 document.getElementById('mpurpose').innerHTML = purpose;
//                 document.getElementById('mdatecreated').innerHTML = date_created;
//                 // sessionStorage.setItem('token', data.token);
//                 // alert("Message : "+ data.Message);
//                 // document.getElementById("call").innerHTML = "Success :" + data.Message;
//                 // window.location.href = './viewdiaries.html';
//             }
//         })
//         .catch(function (error) {
//             console.log('Request failure: ', error);
//         });
// }
