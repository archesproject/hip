define(['jquery', 'underscore', 'views/forms/base', 'views/forms/sections/branch-list'], function ($, _, BaseForm, BranchList) {
    return BaseForm.extend({
        initialize: function() {
			var nameBrachList;
            var self = this;

            BaseForm.prototype.initialize.apply(this);

            nameBranchList = new BranchList({
                el: this.$el.find('#measurement-section')[0],
                viewModel: this.viewModel,
                key: 'MEASUREMENT_TYPE_E55',
                validateBranch: function (data) {
                    // currently we are using the string 'Primary' as the key for the type... this is very brittle and should be enhanced
                    var primaryLabel = 'Primary',
                        valid = data.VALUE_OF_MEASUREMENT_E60__value ? true : false;
                    if (data.MEASUREMENT_TYPE_E55__label === primaryLabel) {
                        _.each(self.viewModel[nameBranchList.key](), function (item) {
                            if (item.MEASUREMENT_TYPE_E55__label === primaryLabel) {
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

