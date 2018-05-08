'use strict';
module.exports = function(httpsApp) {

  // keys Routes
  httpsApp.route('/')
    .get( function(req, res) {
    res.sendFile(path.join(__dirname + '/public/index.html'));
    })
};
