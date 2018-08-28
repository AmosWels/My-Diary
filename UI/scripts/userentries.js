function getentries() {
    let Token = localStorage.getItem("token");
    let url = "http://127.0.0.1:5000/api/v1/entries";

    fetchfunction(url, Token)
        .then(function (data) {
            if (data.Message === "You haven't created any entries yet. Please create first.") {
                document.getElementById("result").innerHTML = "Message : " + data.Message;
            } else if (data.entries != "") {
                var object = data.entries;
                var table = document.getElementsByTagName("table")[0];
                var i = 0;
                var j = 1;
                var objectlength = object.length;
                ({ i, j } = inserttabledata(i, j, objectlength, object, table));
            } else if (data.msg === "Token has expired") {
                alert("Message : " + data.msg + "\n Please Login again");
                window.location.href = "./index.html";
            }
        })
        .catch(function (error) {
            console.log('Request failure: ', error);
        });
}

function fetchfunction(url, Token) {
    return fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${Token}`
        }
    })
        .then(function (response) {
            return response.json();
        });
}

function inserttabledata(i, j, objectlength, object, table) {
    for (i, j; i < objectlength, j <= objectlength; i++ , j++) {
        var id = object[i].id;
        var name = object[i].name;
        var due_date = object[i].due_date;
        var type = object[i].type;
        var purpose = object[i].purpose;
        var date_created = object[i].date_created;
        let dt2 = new Date(due_date);
        let dt1 = new Date(date_created);
        var days = Math.floor((Date.UTC(dt2.getFullYear(), dt2.getMonth(), dt2.getDate()) - Date.UTC(dt1.getFullYear(), dt1.getMonth(), dt1.getDate())) / (1000 * 60 * 60 * 24));
        var newRow = table.insertRow(table.rows.length);
        var cel1 = newRow.insertCell(0);
        var cel2 = newRow.insertCell(1);
        var cel3 = newRow.insertCell(2);
        var cel4 = newRow.insertCell(3);
        var cel5 = newRow.insertCell(4);
        var cel6 = newRow.insertCell(5);
        var cel7 = newRow.insertCell(6);
        var cel8 = newRow.insertCell(7);
        cel1.innerHTML = j + ".";
        cel2.innerHTML = name;
        cel3.innerHTML = due_date;
        cel4.innerHTML = type;
        cel5.innerHTML = purpose;
        cel6.innerHTML = date_created;
        cel7.innerHTML = days;
        let link = document.createElement("a");
        let url = "./modifydiary.html?id=" + id;
        link.setAttribute("href", url);
        link.innerHTML = "Actions";
        cel8.appendChild(link);
    }
    return { i, j };
}

function getuser() {
    let Token = localStorage.getItem("token");
    let url = "http://127.0.0.1:5000/api/v1/authuser";

    fetchfunction(url, Token)
        .then(function (data) {
            if (data.user != "") {
                var object = data.user;
                var i = 0;
                var objectlength = object.length;
                for (i; i < objectlength; i++) {
                    var id = object[i].id;
                    var name = object[i].username;
                    document.getElementById("name").innerHTML = "Username : " + name;
                }
            } else if (data.msg === "Token has expired") {
                alert("Message : " + data.msg + "\n Please Login again");
                window.location.href = "./index.html";
            }
        })
        .catch(function (error) {
            console.log('Request failure: ', error);
        });
}

function createprofile() {
    let Token = localStorage.getItem('token');
    let url = 'http://127.0.0.1:5000/api/v1/authuser/profile';
    let { surname, givenname, email, number } = getprofileinput();
    fetchuserprofile(url, Token, surname, givenname, email, number)
        .then(function (data) {
            if (data.Message === "your Profile has been succesfully Added!") {
                alert("Message : " + data.Message);
                window.location.href = './userprofile.html';
            } else if (data.msg === "Token has expired") {
                alert("Message : " + data.msg + "\n Please Login again");
                window.location.href = './index.html';
            }
            else {
                document.getElementById("prof").innerHTML = "Fail : " + data.Message;
            }
        })
        .catch(function (error) {
            console.log('Request failure: ', error);
        });
    return false;
}

function getprofileinput() {
    let surname = document.getElementById("surname").value;
    let givenname = document.getElementById("givenname").value;
    let email = document.getElementById("email").value;
    let number = document.getElementById("number").value;
    return { surname, givenname, email, number };
}

function fetchuserprofile(url, Token, surname, givenname, email, number) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'Authorization': `Bearer ${Token}`
        },
        body: JSON.stringify({
            surname: surname, givenname: givenname, email: email, phonenumber: number
        })
    })
        .then(function (response) {
            return response.json();
        });
}

function updateprofile() {
    let Token = localStorage.getItem('token');
    let url = 'http://127.0.0.1:5000/api/v1/authuser/profile';
    let { surname1, givenname1, email1, number1 } = getupdateinput();
    fetchprofileupdate(url, Token, surname1, givenname1, email1, number1)
        .then(function (data) {
            if (data.Message === "your Profile has been succesfully modified!") {
                alert("Message : " + data.Message);
                window.location.href = 'userprofile.html';
            } else if (data.msg === "Token has expired") {
                alert("Message : " + data.msg + "\n Please Login again");
                window.location.href = './index.html';
            } else {
                document.getElementById("prof").innerHTML = "Fail : " + data.Message;
            }
        })
        .catch(function (error) {
            console.log('Request failure: ', error);
        });
    return false;
}

function getupdateinput() {
    let surname1 = document.getElementById("surname").value;
    let givenname1 = document.getElementById("givenname").value;
    let email1 = document.getElementById("email").value;
    let number1 = document.getElementById("number").value;
    return { surname1, givenname1, email1, number1 };
}

function fetchprofileupdate(url, Token, surname1, givenname1, email1, number1) {
    return fetch(url, {
        method: 'PUT',
        headers: {
            'Content-type': 'application/json',
            'Authorization': `Bearer ${Token}`
        },
        body: JSON.stringify({
            surname: surname1, givenname: givenname1, email: email1, phonenumber: number1
        })
    })
        .then(function (response) {
            return response.json();
        });
}

getfullprofile()
function getfullprofile() {
    let Token = localStorage.getItem('token');
    let url = 'http://127.0.0.1:5000/api/v1/authuser/profile';
    fetchfunction(url, Token)
        .then(function (data) {
            if (data.Message != "No user found") {
                document.getElementById('profileheader').innerHTML = 'Edit Profile Data';
                let object = data.user;
                var i = 0;
                var objectlength = object.length;
                for (i; i < objectlength; i++) {
                    let id = object[i].id;
                    let surname = object[i].surname;
                    let givenname = object[i].given_name;
                    let email = object[i].email;
                    let number = object[i].phone_number;
                    getuserprofile(surname, givenname, email, number); }
            } else if (data.msg === "Token has expired") {
                alert("Message : " + data.msg + "\n Please Login again");
                window.location.href = "./index.html";
            } else if (data.Message === "No user found") {
                document.getElementById('profileheader').innerHTML = 'Add Profile Data'
            } else { }
        })        .catch(function (error) {
            console.log('Request failure: ', error);
        });
}

function getuserprofile(surname, givenname, email, number) {
    document.getElementById("dataprofile").style.display = "";
    document.getElementById("usurname").innerHTML = "Surname: " + surname;
    document.getElementById("ugiven").innerHTML = "Given name: " + givenname;
    document.getElementById("uemail").innerHTML = "Email: " + email;
    document.getElementById("unumber").innerHTML = "Phone: " + number;

    oFormObject = document.forms['addprofile'];
    oFormObject.elements["surname"].value = surname;
    oFormObject.elements["givenname"].value = givenname;
    oFormObject.elements["email"].value = email;
    oFormObject.elements["number"].value = number;
}

function getentrycount() {
    let Token = localStorage.getItem("token");
    let url = "http://127.0.0.1:5000/api/v1/authuser/countentry";

    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${Token}`
        }
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.entries != "") {
                let object = data.entries;
                let number = object[0].number;
                document.getElementById("entrycount").innerHTML = "Diary Entries : " + number;
            } else if (data.msg === "Token has expired") {
                alert("Message : " + data.msg + "\n Please Login again");
                window.location.href = "./index.html";
            }
        })
        .catch(function (error) {
            console.log('Request failure: ', error);
        });

}