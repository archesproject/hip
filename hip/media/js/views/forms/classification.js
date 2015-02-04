define(['jquery', 'underscore', 'views/forms/base', 'views/forms/sections/branch-list'], function ($, _, BaseForm, BranchList) {
    return BaseForm.extend({
        initialize: function() {
            BaseForm.prototype.initialize.apply(this);
        }
    });
});
