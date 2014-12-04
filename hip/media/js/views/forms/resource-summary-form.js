define(['jquery', 'underscore', 'knockout-mapping', 'views/forms/base', 'views/forms/sections/branch-list'], function ($, _, koMapping, BaseForm, BranchList) {
    return BaseForm.extend({
        initialize: function() {
			var nameBrachList;
            var self = this;

            BaseForm.prototype.initialize.apply(this);

            nameBranchList = new BranchList({
                el: this.$el.find('#names-section')[0],
                viewModel: this.viewModel,
                key: 'NAME_E41',
                validateBranch: function (data) {
                    // currently we are using the string 'Primary' as the key for the type... this is very brittle and should be enhanced
                    var primaryLabel = 'Primary',
                        valid = data.NAME_E41__value ? true : false;
                    if (data.NAME_TYPE_E55__label === primaryLabel) {
                        _.each(self.viewModel[nameBranchList.key](), function (item) {
                            if (item.NAME_TYPE_E55__label === primaryLabel) {
                                valid = false;
                            }
                        });
                    }
                    return valid;
                }
            });
            this.branchLists.push(nameBranchList);

            this.viewModel.HERITAGE_RESOURCE_TYPE_E55 = koMapping.fromJS(this.viewModel.HERITAGE_RESOURCE_TYPE_E55);
        }
    });
});