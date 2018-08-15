//sampleUser.json is replaced by an API endpoint.

//Using ES6 arrow function 
var Token = sessionStorage.getItem('Token');

var url = 'http://127.0.0.1:5000/api/v1/entries';
fetch(url,{
    method: 'GET',
    headers: {
        'Authorization':'Bearer {}'.format(Token),
        'Content-type': 'application/json'
    } })
.then((res) => { return res.json() })
.then((data) => {
    let result = `<h2> Random User Info From Jsonplaceholder API</h2>`;
    data.forEach((entry) => {
        const { id, name, due_date, type, purpose, date_created } = entry
        result +=
            `<tr onclick="location.href = 'viewdiarycontent.html'">
                    <td style="width: 300px;">${name}</td>
                    <td>${date_created}</td>
                    <td>${type}</td>
                    <td>${purpose}</td>
                    <td>${due_date}</td>
                </tr> `;
                document.getElementById('call').innerHTML = result;
            });
        })