var express = require("express")
var mongoose = require('mongoose');
var Key = require('./model/key_model')
var bodyParser = require('body-parser')
mongoose.Promise = require('bluebird');

var path = require('path')
var app = express();

app.use(express.static(path.join(__dirname, 'public')));


console.log('\n\n--- Node Version: ' + process.version + ' ---');


var index = require('./routes/index');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.use('/', index)

var routes = require('./routes/key_routes')
routes(app)

// Start node server listening on specified port -----

console.log('HTTP server listening on port 8080');

app.listen(8080);

console.log("Initializing mongo database");

// var uri = "mongodb+srv://cecs378:cecs378@cecs-378-d5nhx.mongodb.net/test"
var uri = "mongodb://localhost/server"

mongoose.Promise = global.Promise;
mongoose.connect(uri).catch(function (err) {
    console.log("Error connecting to server: ", err);
    process.exit(1);
});
