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
            //'': 'index',
            // Default
            '*actions': 'defaultAction'
        },

        index: function() {
            // Show sports table.
            // var sportsListView = new SportsListView()
        }
    
    });

    var initialize = function() {
        var app_router = new AppRouter;
        app_router.on('route:defaultAction', function (actions) {
            // We have no matching route, lets display the home page 
            var sportListView = SportListView;
            sportListView.render();
        });

        Backbone.history.start();
    };

    return { 
        initialize: initialize
    };
});
