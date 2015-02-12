define(['jquery', 'underscore', 'views/forms/base', 'views/forms/sections/branch-list'], function ($, _, BaseForm, BranchList) {

    return BaseForm.extend({

        initialize: function() {
            var conditionTypeBranchList;
            var self = this;

            //Show and hide Upload Wizard.  
            $("#start-upload").click(function(){ handleWizard(); return false; });
            $("#save-upload").click(function(){
                handleWizard();
                saveWizard(); 
                return false; 
            });
            $("#cancel-upload").click(function(){ handleWizard(); return false; });

            function handleWizard() {    
                $( ["#related-files-list", "#upload-wizard"].join(",") ).toggle(300);
                $( ["#cancel-upload","#save-upload","#start-upload"].join(",")  ).toggle();
            }

            function saveWizard() {    
                $( ["#completed-evaluations"].join(",")  ).toggle(300);
                $( ["#related-files"].join(",")  ).css("display", "block");
                $( ["#no-evaluations", "#no-files"].join(",")  ).css("display", "none");
            }

            BaseForm.prototype.initialize.apply(this);

            conditionTypeBranchList = new BranchList({
                el: this.$el.find('#condition-section')[0],
                viewModel: this.viewModel,
                key: 'CONDITION_TYPE_E55',
                validateBranch: function (data) {
                    var valid = true;
                    if (data.CONDITION_TYPE_E55__label === '') {
                        valid = false;
                    }
                    return valid;
                }
            });
            this.branchLists.push(conditionTypeBranchList);
        }
    });
});