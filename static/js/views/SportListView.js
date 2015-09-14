define([
    'jquery',
    'underscore',
    'backbone',
    'collections',
    'views/TableView'
], function ($, _, Backbone, Collections, TableView) {
    var SportListView = TableView.extend({
        el: $('#sport-list'),
        table_headers: ['Sport title', 'Sport description'],
        fields: ['name', 'description'],
        initialize: function() {
            this.collection = new Collections.Sports()
            this.collection.on('change', this.render, this);
        },
        render: function() {
            TableView.prototype.render.apply(this)
        }
    })
    return SportListView;
});
