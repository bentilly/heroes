define([
  'underscore',
  'backbone',
], function(_, Backbone) {

  var HomeModel = Backbone.Model.extend({
    url: 'http://localhost:8080/users/config/',
    defaults: {
    },

    initialize: function () {
        this.fetch()
    },

  });

  	return HomeModel;

});
