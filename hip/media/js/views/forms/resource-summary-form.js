define(['jquery', 'views/forms/base', 'views/forms/sections/branch-list'], function ($, BaseForm, BranchList) {
    return BaseForm.extend({
        initialize: function() {
            var self = this;

            BaseForm.prototype.initialize.apply(this);

            new BranchList({
                el: this.$el.find('#names-section')[0],
                viewModel: this.viewModel,
                key: 'NAME_E41',
                pkField: 'NAME_E41__value'
            });
        }
    });
});