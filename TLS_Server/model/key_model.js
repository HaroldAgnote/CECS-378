'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var KeySchema = new Schema({
  name: {
    type: String,
    required: 'Kindly enter the name of the key'
  },
  Created_date: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('Keys', KeySchema);
