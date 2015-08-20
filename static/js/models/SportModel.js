define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    var SportModel = Backbone.Model.extend({
        url: '/sports',
        defaults: {
            name: '',
            description: '',
            link: ''
        },
    })
    return SportModel
});
