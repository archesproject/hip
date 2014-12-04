define(['jquery', 'underscore', 'views/forms/base', 'views/forms/sections/branch-list'], function ($, _, BaseForm, BranchList) {
    return BaseForm.extend({
        initialize: function() {
			var nameBrachList;
            var self = this;

            BaseForm.prototype.initialize.apply(this);

            this.branchLists.push(new BranchList({
                el: this.$el.find('#measurement-section')[0],
                viewModel: this.viewModel,
                key: 'MEASUREMENT_TYPE_E55'
            }));
        }
    });
});

