define(['jquery', 'backbone', 'views/forms/base'], function ($, Backbone, BaseForm) {
    return BaseForm.extend({
        initialize: function() {
            BaseForm.prototype.initialize.apply(this);
        }
    });
});