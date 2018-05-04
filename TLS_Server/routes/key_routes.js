'use strict';
module.exports = function(app) {
  var keys = require('../controller/key_controller');

  // keys Routes
  app.route('/keys')
    .get(keys.list_all_keys)
    .post(keys.create_a_key);


  app.route('/keys/:keyId')
    .get(keys.read_a_key)
    .put(keys.update_a_key)
    .delete(keys.delete_a_key);
};
