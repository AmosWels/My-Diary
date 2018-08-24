// document.getElementById('getData').addEventListener('submit', getentries);
function getentries() {
    // e.preventDefault();
    let Token = localStorage.getItem('token');
    let url = 'http://127.0.0.1:5000/api/v1/entries';

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
                    
                    dt2 = new Date(due_date);
                    dt1 = new Date(date_created);
                    var days = Math.floor((Date.UTC(dt2.getFullYear(), dt2.getMonth(), dt2.getDate()) - Date.UTC(dt1.getFullYear(), dt1.getMonth(), dt1.getDate()) ) /(1000 * 60 * 60 * 24));

                    var newRow = table.insertRow(table.rows.length);
                    var cel1 = newRow.insertCell(0);
                    var cel2 = newRow.insertCell(1);
                    var cel3 = newRow.insertCell(2);
                    var cel4 = newRow.insertCell(3);
                    var cel5 = newRow.insertCell(4);
                    var cel6 = newRow.insertCell(5);
                    var cel7 = newRow.insertCell(6);
                    var cel8 = newRow.insertCell(7);
                    var cel9 = newRow.insertCell(8);

                    cel1.innerHTML = j + '.';
                    cel2.innerHTML = name;
                    cel3.innerHTML = due_date;
                    cel4.innerHTML = type;
                    cel5.innerHTML = purpose;
                    cel6.innerHTML = date_created;
                    cel7.innerHTML = days;
                    let link=document.createElement('a');
                    let url='./modifydiary.html?id='+id;
                    link.setAttribute('href',url);
                    link.innerHTML='Actions';
                    cel8.appendChild(link);
                    cel9.innerHTML = '<a href="" onclick"deleteentry();">Delete</a>';
                    

                }
            } else if(data.msg === "Token has expired") {
                alert("Message : "+ data.msg +"\n Please Login again");
                window.location.href = './index.html';
            };
        });
}

// function deleteentry(id) {
//     let Token = localStorage.getItem('token');
//     let url = 'http://127.0.0.1:5000/api/v1/entries/'+id;
//     fetch(url, {
//         method: 'DELETE',
//         headers: {
//             'Content-Type': 'application/json',
//             'Authorization': `Bearer ${Token}`
//         },
//         // body: JSON.stringify({
//         //     due_date: newduedate, name: newname, purpose: newpurpose, type: newtype
//         // })
//     })
//         .then(function (response) {
//             return response.json();
//         })
//         .then(function (data) {
//             if (data.Message === "Deleted your entry succesfully!") {
//                 alert("Message : " + data.Message);
//                 window.location.href = './viewdiaries.html';
//             } else if (data.msg === "Token has expired") {
//                 // document.getElementById("result").innerHTML = "Message : " + data.msg;
//                 alert("Message : " + data.msg + "\n Please Login again");
//                 window.location.href = './index.html';
//             } else {
//                 document.getElementById("call").innerHTML = "Fail : " + data.Message;
//             }
//         })
//         .catch(function (error) {
//             console.log('Request failure: ', error)
//         });

// }
