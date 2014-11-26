define(['jquery', 'views/forms/base', 'views/forms/sections/branch-list'], function ($, BaseForm, BranchList) {
    return BaseForm.extend({
        initialize: function() {
            var self = this,
                nameBranchList;

            BaseForm.prototype.initialize.apply(this);

            nameBranchList = new BranchList({
                el: this.$el.find('#names-section')[0],
                viewModel: this.viewModel,
                key: 'NAME_E41',
                pkField: 'NAME_E41__entityid',
                validateBranch: function (data) {
                    return data.NAME_E41__value;
                }
            });
        }
    });
});