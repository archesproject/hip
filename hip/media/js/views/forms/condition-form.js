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
                    // currently we are using the string 'Primary' as the key for the type... this is very brittle and should be enhanced
                    if (data.CONDITION_TYPE_E55__label === primaryLabel) {
                        _.each(self.viewModel[nameBranchList.key](), function (item) {
                            if (item.CONDITION_TYPE_E55__label === primaryLabel) {
                                valid = false;
                            }
                        });
                    }
                    return valid;
                }
            });
            this.branchLists.push(nameBranchList);
        }
    });
});