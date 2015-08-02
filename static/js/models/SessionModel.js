define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    var SessionModel = Backbone.Model.extend({
        url: '/users/config/',
        initialize: function () {
            this.fetch()
        },
    })

    return SessionModel
});
