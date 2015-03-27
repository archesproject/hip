define(['jquery', 
    'underscore', 
    'views/forms/wizard-base', 
    'views/forms/entity-list',
    'views/forms/entity',
    'bootstrap-datetimepicker',
    'summernote'], function ($, _, WizardBase, EntityList, Entity, datetimepicker, summernote) {

    return WizardBase.extend({
        initialize: function() {
            WizardBase.prototype.initialize.apply(this);

            // var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
            // date_picker.on('dp.change', function(evt){
            //     $(this).find('input').trigger('change'); 
            // });



            // conditionBranch = this.addBranchList(new EntityGraph({
            //     el: this.$el.find('#condition-section')[0],
            //     data: this.data['CONDITION_ASSESSMENT.E14'],
            //     dataKey: 'CONDITION_ASSESSMENT.E14',
            //     validateBranch: function (data) {
            //         var valid = true;
            //         return valid;
            //     }
            // }));

            // conditionBranch = this.addBranchList(new EntityList({
            //     el: this.$el.find('#condition-section')[0],
            //     data: this.data['CONDITION_ASSESSMENT.E14'].child_entities,
            //     domains: this.data['CONDITION_ASSESSMENT.E14'].domains,
            //     //dataKey: 'CONDITION_ASSESSMENT.E14',
            //     defaults: [],
            //     validateBranch: function (data) {
            //         var valid = true;
            //         return valid;
            //     }
            // }));

            conditionBranch = this.addBranchList(new Entity({
                el: this.$el.find('#condition-section')[0],
                data: this.data['CONDITION_ASSESSMENT.E14'],
                //domains: this.data['CONDITION_ASSESSMENT.E14'].domains,
                //dataKey: 'CONDITION_ASSESSMENT.E14',
                defaults: [],
                single_instance_entities: [
                    'DATE_CONDITION_ASSESSED.E49',
                    'CONDITION_TYPE.E55',
                    'CONDITION_DESCRIPTION.E62'
                ],
                validateBranch: function (data) {
                    var valid = true;
                    return valid;
                },
                editCondition: function(entity){
                    entity.parent.editing(true);
                }
            }));

            // var x = conditionBranch.createSubBranch(BranchList, {
            //     el: this.$el.find('#threat-section')[0],
            //     dataKey: 'THREAT.E55',
            //     validateBranch: function (data) {
            //         var valid = true;
            //         return valid;
            //     }
            // })

            //this.addBranchList();


        }
    });
});