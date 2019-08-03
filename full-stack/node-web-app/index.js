var http = require('http')
var url = require('url')
var show = require('./showPage')
const express = require('express');
const app = new express();

app.get('/', function(request, response) {
    response.sendFile('C:\\Users\\kisho\\Documents\\git\\random-projects\\full-stack\\node-web-app\\index.html')
});
app.get('/finder', function(request, response) {
    response.sendFile('C:\\Users\\kisho\\Documents\\git\\random-projects\\full-stack\\node-web-app\\finder.html')
});
app.listen(8888);

// http.createServer(onRequest).listen(8888);
// console.log('Server has started');

// function onRequest(request, response){
// //   var pathName = url.parse(request.url).pathname
// //   console.log('pathname: ' + pathName);
// //   show.showPage(response, pathName);
//     app.get('/', function(request, response) {
//         response.sendFile('index.html')
//     });
// }

