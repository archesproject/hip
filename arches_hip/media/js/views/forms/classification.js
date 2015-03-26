define(['jquery', 
    'underscore', 
    'summernote', 
    'views/forms/base', 
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker'], function ($, _, summernote, BaseForm, BranchList) {
    return BaseForm.extend({
        initialize: function() {
            BaseForm.prototype.initialize.apply(this);

            var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
            date_picker.on('dp.change', function(evt){
                $(this).find('input').trigger('change'); 
            });

            this.addBranchList(new BranchList({
                el: this.$el.find('#classification-section')[0],
                data: this.data,
                dataKey: 'PHASE_TYPE_ASSIGNMENT.E17',
                validateBranch: function (nodes) {
                    return true;
                    return this.validateHasValues(nodes);
                }
            }));
            this.addBranchList(new BranchList({
                el: this.$el.find('#component-section')[0],
                data: this.data,
                dataKey: 'COMPONENT.E18',
                validateBranch: function (nodes) {
                    return true;
                    return this.validateHasValues(nodes);
                }
            }));
            this.addBranchList(new BranchList({
                el: this.$el.find('#modification-section')[0],
                data: this.data,
                dataKey: 'MODIFICATION_EVENT.E11',
                validateBranch: function (nodes) {
                    return true;
                    return this.validateHasValues(nodes);
                }
            }));
        }
    });
});
