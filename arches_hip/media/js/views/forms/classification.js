define(['jquery', 
    'underscore', 
    'views/forms/base', 
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker'], function ($, _, BaseForm, BranchList) {
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
        }
    });
});
