define(['jquery', 'summernote', 'views/forms/base', 'views/forms/sections/branch-list', ], function ($, summernote, BaseForm, BranchList) {
    return BaseForm.extend({
        initialize: function() {
            var descriptionBranchList;
            var self = this;

            BaseForm.prototype.initialize.apply(this);

            descriptionBranchList = new BranchList({
                el: this.$el.find('#description-section')[0],
                viewModel: this.viewModel,
                key: 'DESCRIPTION_E62',
                pkField: 'DESCRIPTION_E62__entityid'
            })
            this.branchLists.push(descriptionBranchList);
        }
    });
});