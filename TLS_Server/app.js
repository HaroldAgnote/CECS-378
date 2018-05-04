var express = require('express');
var http = require('http')
var https = require('https')
var mongoose = require('mongoose');
var bodyParser = require('body-parser')

var path = require('path')
var fs = require('fs')

var Key = require('./model/key_model')

mongoose.Promise = require('bluebird');


var helmet = require('helmet')
var ONE_YEAR = 31536000000;

var routes = require('./routes/key_routes')

var httpApp = express();
var httpsApp = express();

var httpAppPort = 8080;
var httpsAppPort = 8443;

httpApp.use(bodyParser.urlencoded({ extended: true }));
httpApp.use(bodyParser.json());

httpsApp.use(helmet.hsts({
    maxAge: ONE_YEAR,
    includeSubdomains: true,
    force: true}));

httpsApp.use(bodyParser.urlencoded({ extended: true }));
httpsApp.use(bodyParser.json());

routes(httpApp)
routes(httpsApp)

var cipher = ['ECDHE-ECDSA-AES256-GCM-SHA384',
'ECDHE-RSA-AES256-GCM-SHA384',
'ECDHE-RSA-AES256-CBC-SHA384',
'ECDHE-RSA-AES256-CBC-SHA256',
'ECDHE-ECDSA-AES128-GCM-SHA256',
'ECDHE-RSA-AES128-GCM-SHA256',
'DHE-RSA-AES128-GCM-SHA256',
'DHE-RSA-AES256-GCM-SHA384',
'!aNULL',
'!MD5',
'!DSS'].join(':');

httpApp.get("*", function(req, res, next){
    res.redirect('https://' + req.headers.host + req.url);
})

httpsApp.get('/', function(req, res){
res.send('You are in the right place.');
});

var options = {
    key: fs.readFileSync('privkey.pem'),
    cert: fs.readFileSync('fullchain.pem'),
    ciphers: cipher
};

http.createServer(httpApp).listen(8080);
https.createServer(options, httpsApp).listen(8443);

console.log("Server running on localhost");
console.log("http running on port " + httpAppPort); 
console.log("https running on port " + httpsAppPort); 

console.log("Initializing mongo database");

var uri = "mongodb://localhost/server"

mongoose.Promise = global.Promise;
mongoose.connect(uri).catch(function (err) {
    console.log("Error connecting to server: ", err);
    process.exit(1);
});
