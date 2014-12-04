define(['jquery', 'underscore', 'knockout-mapping', 'views/forms/base', 'views/forms/sections/branch-list'], function ($, _, koMapping, BaseForm, BranchList) {
    return BaseForm.extend({
        initialize: function() {
			var nameBrachList;
            var self = this;

            BaseForm.prototype.initialize.apply(this);

            this.branchLists.push(new BranchList({
                el: this.$el.find('#measurement-section')[0],
                viewModel: this.viewModel,
                key: 'MEASUREMENT_TYPE_E55',
                validateBranch: function (data) {
                    var valid = true;

                    if (data.VALUE_OF_MEASUREMENT_E60__value === '') {
                                valid = false;
                    }
                    if (data.MEASUREMENT_TYPE_E55__label === '') {
                                valid = false;
                    }
                    if (data.UNIT_OF_MEASUREMENT_E55__label === '') {
                                valid = false;
                    }
                    return valid;
                }
            }));

            this.viewModel.HERITAGE_RESOURCE_TYPE_E55 = koMapping.fromJS(this.viewModel.HERITAGE_RESOURCE_TYPE_E55);
        }
    });
});

