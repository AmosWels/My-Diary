const baseurl = 'https://mydiario3.herokuapp.com';
// const baseurl = 'http://127.0.0.1:5000';

function logout() {
	localStorage.removeItem('token');
	window.location.href = 'index.html';
}
