document.getElementById('getData').addEventListener('submit', getentries);
function getentries(e) {
    e.preventDefault();
    var Token = sessionStorage.getItem('token');
    // var Token = Window.getItem('Token');
    // var Token = window.localStorage.getItem('token');

    var url = 'http://127.0.0.1:5000/api/v1/entries';
    fetch(url, {
        method:'GET',
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
                document.getElementById('result').innerHTML = "Success :" + data.Message; }
            if (data.entries != ""){
                // document.getElementById('result').innerHTML = "Success :" + data.entries;
            // } else{
            //     document.getElementById('result').innerHTML = "Success :" + data.Message;
                let result;
                data.forEach((entry) => {
                    const { id, name, due_date, type, purpose, date_created } = entry
                    result +=
                        `<div>
                    <h5> User ID: ${id} </h5>
                        <ul>
                            <li> User Full Name : ${name}</li>
                            <li> User Email : ${due_date} </li>
                            <li> User Address : ${type} </li>
                            <li> User Address : ${purpose} </li>
                            <li> User Address : ${date_created} </li>
                        </ul>
                    </div>`;
                    document.getElementById('result').innerHTML = result;
                });
            }
        })
}
 //     result +=
                //         `<tr onclick="location.href = './viewdiarycontent.html'">
                //                 <td style="width: 300px;">${name}</td>
                //                 <td>${date_created}</td>
                //                 <td>${type}</td>
                //                 <td>${purpose}</td>
                //                 <td>${due_date}</td>
                //             </tr> `;
                //     document.getElementById('result').innerHTML = result;
                // });