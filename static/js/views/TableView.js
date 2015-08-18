define([
    'jquery',
    'underscore',
    'backbone',
    'text!templates/table.html'
], function($, _, Backbone, tableTemplate){
    var TableView = Backbone.View.extend({
        template: tableTemplate,
        table_headers: [],
        fields: [],

        render: function() {
            var data = {
                items: this.collection.toJSON(),
                table_headers: this.table_headers,
                fields: this.fields,
                _: _ 
            };
            var compiledTemplate = _.template(this.template)( data );
            this.$el.html(compiledTemplate);
        }
    });

    return TableView;
});
