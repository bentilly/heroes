define([
    'jquery',
    'underscore',
    'backbone',
    'models/SportModel',
], function($, _, Backbone, SportModel){
    var Sports = Backbone.Collection.extend({
        url: '/sports/',
        model: SportModel,
        initialize: function () {
            this.fetch({async: false})
        },

        parse: function (response) {
            var that = this;
            response.result.forEach(function (item) {
                that.push(new SportModel({name: item.name, id: item.id,
                                          description: item.description}))
            });
            return that.models;
        }
    });
    return {'Sports': Sports};
});