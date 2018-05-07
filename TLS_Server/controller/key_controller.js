'use strict';

var mongoose = require('mongoose'),
  Key = mongoose.model('Keys');

exports.list_all_keys = function(req, res) {
  Key.find({}, function(err, key) {
    if (err)
      res.send(err);
    res.json(key);
    res.end();
  });
};

exports.get_a_key = function(req, res) {
    console.log("Received request: " + req);
    console.log("Getting key...");
    var headers = req.headers
    var header_string = JSON.stringify(req.headers);
    var public_key_string = headers.public_key;
    console.log(header_string);
    console.log("\nPublic Key: " + public_key_string);
    
    Key.find({public_key: public_key_string}, function(err, key) {
        if (err)
            res.send(err);
        res.json(key);
        res.end();
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
    res.end();
  });
};


exports.read_a_key = function(req, res) {
  Key.findById(req.params.keyId, function(err, key) {
    if (err)
      res.send(err);
    res.json(key);
    res.end();
  });
};


exports.update_a_key = function(req, res) {
  Key.findOneAndUpdate({_id: req.params.keyId}, req.body, {new: true}, function(err, key) {
    if (err)
      res.send(err);
    res.json(key);
    res.end();
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

