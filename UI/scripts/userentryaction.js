document.getElementById('getentryData').addEventListener('submit', getentry);

function extractid(){
    let url=window.location.search.substring(1);
    let variables=url.split('&');
    for(var i=0;i<variables.length;i++){
        var parname=variables[i].split('=');
        if(parname[0]=='id'){
            return parname[1];
        }
    }
    return('wrong URL');
}
getentry();
function getentry() {
    // e.preventDefault();
    var Token = localStorage.getItem('token');
    let id =extractid();
    if(id==='wrong URL'){
        
        return(id);

    }
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
                // document.getElementById("result").innerHTML = "Message : " + data.Message;
                alert("Message : "+ data.Message +"\n Entry id : "+ id);
                window.location.href = './modifydiary.html';
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
                sessionStorage.setItem('id',id);
                }
            } else if(data.msg === "Token has expired") {
                // document.getElementById("result").innerHTML = "Message : " + data.msg;
                alert("Message : "+ data.msg +"\n Please Login again");
                window.location.href = './index.html';
            };
        });
}