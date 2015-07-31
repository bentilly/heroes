define([
  'underscore',
  'backbone',
], function(_, Backbone) {

  var HomeModel = Backbone.Model.extend({
    url: '/users/config/',
    defaults: {
    },

    initialize: function () {
        this.fetch()
    },

  });

  	return HomeModel;

});
