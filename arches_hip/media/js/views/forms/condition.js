define(['jquery', 
    'underscore', 
    'knockout',
    'views/forms/wizard-base', 
    'views/forms/sections/branch-list',
    'views/forms/entity',
    'bootstrap-datetimepicker',
    'summernote'], function ($, _, ko, WizardBase, BranchList, Entity, datetimepicker, summernote) {

    return WizardBase.extend({
        initialize: function() {
            var self = this;
            WizardBase.prototype.initialize.apply(this);

            var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
            date_picker.on('dp.change', function(evt){
                $(this).find('input').trigger('change'); 
            });

            this.editAssessment = function(branchlist){
                self.switchBranchForEdit(branchlist);
                self.startWorkflow();
            }

            this.deleteAssessment = function(branchlist){
                self.deleteClicked(branchlist);
            }

            ko.applyBindings(this, this.$el.find('#existing-assessments')[0]);

            var currentEditedAssessment = this.getBlankFormData(); //this.data.data[0];
            this.addBranchList(new BranchList({
                data: currentEditedAssessment,
                dataKey: 'CONDITION_ASSESSMENT.E14'
            }));
            this.addBranchList(new BranchList({
                el: this.$el.find('#recommendations-section')[0],
                data: currentEditedAssessment,
                dataKey: 'RECOMMENDATION_TYPE.E55'
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#threats-section')[0],
                data: currentEditedAssessment,
                dataKey: 'THREAT_TYPE.E55'
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#condition-type-section')[0],
                data: currentEditedAssessment,
                dataKey: 'CONDITION_TYPE.E55',
                singleEdit: true,
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#disturbances-section')[0],
                data: currentEditedAssessment,
                dataKey: 'DISTURBANCE_TYPE.E55'
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#description-section')[0],
                data: currentEditedAssessment,
                dataKey: 'CONDITION_DESCRIPTION.E62',
                singleEdit: true
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#date-section')[0],
                data: currentEditedAssessment,
                dataKey: 'DATE_CONDITION_ASSESSED.E49',
                singleEdit: true,
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));


        },

        switchBranchForEdit: function(conditionAssessmentData){
            this.prepareData(conditionAssessmentData);

            _.each(this.branchLists, function(branchlist){
                branchlist.data = conditionAssessmentData;
                branchlist.undoAllEdits();
            }, this);
        },

        prepareData: function(assessmentNode){
            _.each(assessmentNode, function(value, key, list){
                assessmentNode[key].domains = this.data.domains;
            }, this);
            return assessmentNode;
        },

        getBlankFormData: function(){
            return this.prepareData({
                'CONDITION_ASSESSMENT.E14': {
                    'branch_lists': []
                },
                'DISTURBANCE_TYPE.E55': {
                    'branch_lists': []
                },
                'CONDITION_TYPE.E55': {
                    'branch_lists': []
                },
                'THREAT_TYPE.E55': {
                    'branch_lists': []
                },
                'RECOMMENDATION_TYPE.E55': {
                    'branch_lists': []
                },
                'DATE_CONDITION_ASSESSED.E49': {
                    'branch_lists': []
                },
                'CONDITION_DESCRIPTION.E62': {
                    'branch_lists': []
                }
            })
        },

        deleteClicked: function(branchlist) {
            var warningtext = '';

            this.deleted_assessment = branchlist;
            this.confirm_delete_modal = this.$el.find('.confirm-delete-modal');
            this.confirm_delete_modal_yes = this.confirm_delete_modal.find('.confirm-delete-yes');
            this.confirm_delete_modal_yes.removeAttr('disabled');

            warningtext = this.confirm_delete_modal.find('.modal-body [name="warning-text"]').text();
            this.confirm_delete_modal.find('.modal-body [name="warning-text"]').text(warningtext + ' ' + branchlist['DATE_CONDITION_ASSESSED.E49'].branch_lists[0].nodes[0].label.substr(0,10) + ': ' + branchlist['CONDITION_TYPE.E55'].branch_lists[0].nodes[0].label);           
            this.confirm_delete_modal.modal('show');
        }

    });
});