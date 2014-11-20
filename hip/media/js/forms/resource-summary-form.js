define(['jquery', 'backbone'], function ($, Backbone) {
    return Backbone.View.extend({
        initialize: function() {
            console.log(this.$el.html());
        }
    });
});