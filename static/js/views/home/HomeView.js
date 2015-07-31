define([
  'jquery',
  'underscore',
  'backbone',
  'models/home/HomeModel',
  'text!templates/home/homeTemplate.html'
], function($, _, Backbone, HomeModel, homeTemplate){
    var HomeView = Backbone.View.extend({
        el: $("#page"),
        events: {
            'click #login': 'login'
        },
        initialize: function(){
            this.model = new HomeModel();
            this.model.on("change", this.render, this);
        },

        login: function() {
            var that = this;
            this.model.logFunction();
        },

        render: function(){
            var data = {
                user: this.model.toJSON(),
                _: _ 
            };

            var compiledTemplate = _.template( homeTemplate)( data );
            this.$el.html(compiledTemplate);
        }

  });

  return HomeView;
});
