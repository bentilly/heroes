define([
  'underscore',
  'backbone',
], function(_, Backbone) {

  var HomeModel = Backbone.Model.extend({
    url: 'http://localhost:8080/users/config/',
    defaults: {
      loggedIn: false,
    },

    initialize: function () {
    },

    logFunction: function(){
      var onDataHandler = function(that) {
        that.set({'loggedIn': true})
      };

      var onErrorHandler = function() {
      
      };

      if(this.get('loggedIn') !== true){
        this.fetch({ success : onDataHandler(this), error: onErrorHandler() })
      }
      else{
        this.set({'loggedIn': false})
      }

    },

  });

  	return HomeModel;

});
