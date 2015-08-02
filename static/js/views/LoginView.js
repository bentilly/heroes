define([
    'jquery',
    'underscore',
    'backbone',
    'models/SessionModel',
    'text!templates/login.html'
], function($, _, Backbone, SessionModel, loginTemplate){
    var LoginView = Backbone.View.extend({
        el: $("#navigation"),
        initialize: function(){
            this.model = new SessionModel();
            this.model.on('change', this.render, this);
            // this.model.trigger('change', this.model)
        },

        render: function(){
            var data = {
                user: this.model.toJSON(),
                _: _ 
            };
            var compiledTemplate = _.template(loginTemplate)( data );
            this.$el.html(compiledTemplate);
        }
    });

    return LoginView;
});
