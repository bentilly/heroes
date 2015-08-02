// Filename: app.js
define([
    'jquery',
    'underscore',
    'backbone',
    'router', // Request router.js
    'views/LoginView',
], function($, _, Backbone, Router, LoginView) {
    var initialize = function(){
        // initialize user session.
        var loginView = new LoginView()
        loginView.render()

        // initialize router.
        Router.initialize();
    };

    return {
        initialize: initialize
    };
});
