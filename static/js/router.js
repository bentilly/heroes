// Filename: router.js
define([
    'jquery',
    'underscore',
    'backbone',
    'views/SportListView'
], function($, _, Backbone, SportListView) {
    var AppRouter = Backbone.Router.extend({
        routes: {
            // Define some URL routes
            '': 'index',
            // Default
            '*actions': 'defaultAction'
        },

        index: function() {
            console.log('We are on index page.')

            // Show sports table.
            var sportsListView = new SportListView()
            sportsListView.render()
        }
    
    });

    var initialize = function() {
        var app_router = new AppRouter;
        app_router.on('route:defaultAction', function (actions) {
            // We have no matching route, lets display the home page 
        });

        Backbone.history.start();
    };

    return { 
        initialize: initialize
    };
});
