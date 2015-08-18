define([
    'jquery',
    'underscore',
    'backbone',
    'collections',
    'text!templates/sport-list.html'
], function ($, _, Backbone, Collections, sportListTemplate) {
    /*var SportItemView = Backbone.View.extend({
        render: function() {
            var data = this.model.toJSON()
            this.$el.html('<tr><td>'+data.name+'</td>'+'<td>'+data.description+'</td></tr>')
        }
    }) */
    var SportListView = Backbone.View.extend({
        el: $('#sport-list'),
        initialize: function() {
            this.collection = new Collections.Sports()
            this.collection.on('change', this.render, this);
        },

        render: function() {
            var data = {
                sports: this.collection.toJSON(),
                _: _ 
            };
            console.log(data.sports)
            var compiledTemplate = _.template(sportListTemplate)( data );
            this.$el.html(compiledTemplate);
        }
    })
    return SportListView;
});
