define([
    'jquery',
    'underscore',
    'backbone',
    'collections',
    'collectionView'
], function ($, _, Backbone, Collections, collectionView) {
    var SportItemView = Backbone.View.extend({
        render: function() {
            var data = this.model.toJSON()
            this.$el.html('<tr><td>'+data.name+'</td>'+'<td>'+data.description+'</td></tr>')
        }
    })
    var SportListView = new Backbone.CollectionView({
        el: $('#sports-list'),
        selectable: true,
        collection: new Collections.Sports(),
        modelView: SportItemView
    });
    return SportListView;
});
