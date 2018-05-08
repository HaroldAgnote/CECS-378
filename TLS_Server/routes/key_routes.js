'use strict';
module.exports = function(httpsApp) {
  var keys = require('../controller/key_controller');

  // keys Routes
  httpsApp.route('/keys')
    // .get(keys.list_all_keys)
    .get(keys.get_a_key)
    .post(keys.create_a_key);

    httpsApp.route('/payload')
        .get(keys.get_payload);

  httpsApp.route('/MyUnlock')
      .get(keys.get_unlock);
};
