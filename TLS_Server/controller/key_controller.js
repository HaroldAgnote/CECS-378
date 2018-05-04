'use strict';

var mongoose = require('mongoose'),
  Key = mongoose.model('Keys');

exports.list_all_keys = function(req, res) {
  Key.find({}, function(err, key) {
    if (err)
      res.send(err);
    res.json(key);
  });
};

exports.create_a_key = function(req, res) {
    console.log("Received request: ");
    console.log(req.body);
  var new_key = new Key(req.body);
  new_key.save(function(err, key) {
    if (err)
      res.send(err);
    res.json(key);
  });
};


exports.read_a_key = function(req, res) {
  Key.findById(req.params.keyId, function(err, key) {
    if (err)
      res.send(err);
    res.json(key);
  });
};


exports.update_a_key = function(req, res) {
  Key.findOneAndUpdate({_id: req.params.keyId}, req.body, {new: true}, function(err, key) {
    if (err)
      res.send(err);
    res.json(key);
  });
};


exports.delete_a_key = function(req, res) {
  Key.remove({
    _id: req.params.keyId
  }, function(err, key) {
    if (err)
      res.send(err);
    res.json({ message: 'Key successfully deleted' });
  });
};

