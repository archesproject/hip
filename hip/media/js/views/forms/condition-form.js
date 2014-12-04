define(['jquery', 'underscore', 'views/forms/base', 'views/forms/sections/branch-list'], function ($, _, BaseForm, BranchList) {
    return BaseForm.extend({
        initialize: function() {
			var nameBrachList;
            var self = this;

            BaseForm.prototype.initialize.apply(this);

            nameBranchList = new BranchList({
                el: this.$el.find('#condition-section')[0],
                viewModel: this.viewModel,
                key: 'CONDITION_TYPE_E55',
                validateBranch: function (data) {
                    var valid = true;
                    if (data.CONDITION_TYPE_E55__label === '') {
                        valid = false;
                    }
                    return valid;
                }
            });
            this.branchLists.push(nameBranchList);
        }
    });
});