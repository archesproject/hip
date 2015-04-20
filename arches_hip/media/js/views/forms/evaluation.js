define(['jquery', 
    'underscore', 
    'knockout',
    'views/forms/wizard-base', 
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',
    'arches',
    'dropzone',
    'summernote',
    'blueimp-gallery',
    'blueimp-jquery',
    'plugins/bootstrap-image-gallery.min'], function ($, _, ko, WizardBase, BranchList, datetimepicker, arches, dropzone, summernote) {

    return WizardBase.extend({
        initialize: function() {
            WizardBase.prototype.initialize.apply(this);

            var self = this;          
            var currentEditedAssessment = this.getBlankFormData();
            var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});            

            date_picker.on('dp.change', function(evt){
                $(this).find('input').trigger('change'); 
            });


            this.editAssessment = function(branchlist){
                self.switchBranchForEdit(branchlist);
            }

            this.deleteAssessment = function(branchlist){
                self.deleteClicked(branchlist);
            }

            ko.applyBindings(this, this.$el.find('#existing-assessments')[0]);

            this.addBranchList(new BranchList({
                data: currentEditedAssessment,
                dataKey: 'EVALUATION_CRITERIA_ASSIGNMENT.E13'
            }));

            var statusSection = new BranchList({
                el: this.$el.find('#status-section')[0],
                data: currentEditedAssessment,
                dataKey: 'STATUS.E55'
            });
            ko.applyBindings(statusSection, this.$el.find('#status-summary-section')[0]);
            this.addBranchList(statusSection);

            var evaluationSection = new BranchList({
                el: this.$el.find('#evaluation-section')[0],
                data: currentEditedAssessment,
                dataKey: 'EVALUATION_CRITERIA_TYPE.E55',
                showParents: true,
                singleEdit: true
            });
            ko.applyBindings(evaluationSection, this.$el.find('#evaluation-summary-section')[0]);
            this.addBranchList(evaluationSection);


            var eligibilitySection = new BranchList({
                el: this.$el.find('#eligibility-section')[0],
                data: currentEditedAssessment,
                dataKey: 'ELIGIBILITY_REQUIREMENT_TYPE.E55'
            });
            ko.applyBindings(eligibilitySection, this.$el.find('#eligibility-summary-section')[0]);
            this.addBranchList(eligibilitySection);


            var integritySection = new BranchList({
                el: this.$el.find('#integrity-section')[0],
                data: currentEditedAssessment,
                dataKey: 'INTEGRITY_TYPE.E55'
            });
            ko.applyBindings(integritySection, this.$el.find('#integrity-summary-section')[0]);
            this.addBranchList(integritySection);


            var descriptionSection = new BranchList({
                el: this.$el.find('#description-section')[0],
                data: currentEditedAssessment,
                dataKey: 'REASONS.E62',
                singleEdit: true
            });
            ko.applyBindings(descriptionSection, this.$el.find('#description-summary-section')[0]);
            this.addBranchList(descriptionSection);

            var dateEvaluatedSection = new BranchList({
                el: this.$el.find('#date-evaluated-section')[0],
                data: currentEditedAssessment,
                dataKey: 'DATE_EVALUATED.E49',
                singleEdit: true
            });
            ko.applyBindings(descriptionSection, this.$el.find('#date-evaluated-summary-section')[0]);
            this.addBranchList(dateEvaluatedSection);

            var evaluationAssignment = new BranchList({
                data: currentEditedAssessment,
                dataKey: 'EVALUATION_CRITERIA_ASSIGNMENT.E13'
            });
            this.addBranchList(evaluationAssignment);

            },


        validate: function(){
            isValid = true;
            var data = JSON.parse(this.getData());
            if (data['EVALUATION_CRITERIA_TYPE.E55'].length < 1) {
                isValid = false;
            }
            return isValid
        },


        startWorkflow: function() { 
            this.switchBranchForEdit(this.getBlankFormData());
        },

        switchBranchForEdit: function(conditionAssessmentData){
            this.prepareData(conditionAssessmentData);

            _.each(this.branchLists, function(branchlist){
                branchlist.data = conditionAssessmentData;
                branchlist.undoAllEdits();
            }, this);

            this.toggleEditor();
        },

        prepareData: function(assessmentNode){
            _.each(assessmentNode, function(value, key, list){
                assessmentNode[key].domains = this.data.domains;
            }, this);
            return assessmentNode;
        },

        getBlankFormData: function(){
            return this.prepareData({
                'EVALUATION_CRITERIA_TYPE.E55': {
                    'branch_lists': []
                },
                'STATUS.E55': {
                    'branch_lists': []
                },
                'ELIGIBILITY_REQUIREMENT_TYPE.E55': {
                    'branch_lists': []
                },
                'INTEGRITY_TYPE.E55': {
                    'branch_lists': []
                },
                'REASONS.E62': {
                    'branch_lists': []
                },
                'DATE_EVALUATED.E49': {
                    'branch_lists': []
                },
                'EVALUATION_CRITERIA_ASSIGNMENT.E13': {
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
            this.confirm_delete_modal.find('.modal-body [name="warning-text"]').text(warningtext + ' ' + branchlist['EVALUATION_CRITERIA_TYPE.E55'].branch_lists[0].nodes[0].label);         
            this.confirm_delete_modal.modal('show');
        }

    });
});