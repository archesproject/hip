define(['jquery', 
    'underscore', 
    'views/forms/base', 
    'views/forms/sections/branch-list',
    'views/forms/sections/entity-graph',
    'bootstrap-datetimepicker'], function ($, _, BaseForm, BranchList, EntityGraph) {

    return BaseForm.extend({
        initialize: function() {
            BaseForm.prototype.initialize.apply(this);

            var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
            date_picker.on('dp.change', function(evt){
                $(this).find('input').trigger('change'); 
            });

            function handleWizard() {    
                $( ["#related-files-list", "#upload-wizard"].join(",") ).toggle(300);
                $( ["#cancel-upload","#save-upload","#start-upload"].join(",")  ).toggle();
            }

            function saveWizard() {    
                $( ["#completed-evaluations"].join(",")  ).toggle(300);
                $( ["#related-files"].join(",")  ).css("display", "block");
                $( ["#no-evaluations", "#no-files"].join(",")  ).css("display", "none");
            }

            //Show and hide Upload Wizard.  
            $("#start-upload").click(function(){ handleWizard(); return false; });
            $("#save-upload").click(function(){
                handleWizard();
                saveWizard(); 
                return false; 
            });
            $("#cancel-upload").click(function(){ handleWizard(); return false; });

            conditionBranch = this.addBranchList(new EntityGraph({
                el: this.$el.find('#condition-section')[0],
                data: this.data['CONDITION_ASSESSMENT.E41'],
                dataKey: 'CONDITION_ASSESSMENT.E41',
                validateBranch: function (data) {
                    var valid = true;
                    return valid;
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