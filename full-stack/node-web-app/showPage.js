var contents = require('./contents')

function showPage(response, pathName) {
    if (contents.contentMap[pathName]) {
        response.writeHead(200, {'Content-Type': 'text/html'});
        // response.write(contents.contentMap[pathName]);
        response.sendFile('index.html');
        response.end();
    } else {
        response.writeHead(404, {'Content-Type': 'text/html'})
        response.write('404 Page not found');
        response.end();
    }    
}

exports.showPage = showPage;