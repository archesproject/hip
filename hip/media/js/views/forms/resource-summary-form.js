define(['jquery', 'views/forms/base', 'views/forms/sections/branch-list'], function ($, BaseForm, BranchList) {
    return BaseForm.extend({
        initialize: function() {
            var self = this;

            BaseForm.prototype.initialize.apply(this);

            this.$el.find('.resource-type, .name-type').select2();

            new BranchList({
                el: this.$el.find('#names-section')[0],
                viewModel: this.viewModel,
                key: 'NAME_E41',
                pkField: 'NAME_E41__value'
            })

            this.viewModel.editing.NAME_E41.NAME_TYPE_E55__value.subscribe(function(newValue) {
                self.viewModel.editing.NAME_E41.NAME_TYPE_E55__label($('#resource-name-type option:selected').text());
            });
        }
    });
});