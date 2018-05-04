'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var KeySchema = new Schema({
    private_key: {
        type: String,
        default: "No string"
    },
    public_key: {
        type: String,
        default: "No string"
    },
    Created_date: {
        type: Date,
        default: Date.now
    }
});

module.exports = mongoose.model('Keys', KeySchema);
