define(['jquery', 'backbone', 'views/forms/base'], function ($, Backbone, BaseForm) {
    return BaseForm.extend({
        initialize: function() {
            BaseForm.prototype.initialize.apply(this);
            this.$el.find('.resource-type').select2({
                placeholder: "type"
            });
        }
    });
});