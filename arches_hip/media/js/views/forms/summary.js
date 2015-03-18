define(['jquery', 
    'underscore', 
    'knockout-mapping', 
    'views/forms/base', 
    'views/forms/sections/branch-list',
    'bootstrap-datetimepicker',], 
    function ($, _, koMapping, BaseForm, BranchList) {
        return BaseForm.extend({
            initialize: function() {
                console.log('in summary.js initialize');
                BaseForm.prototype.initialize.apply(this);                
                
                var self = this;
                var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
                date_picker.on('dp.change', function(evt){
                    $('#date').trigger('change'); 
                });

                this.addBranchList(new BranchList({
                    el: this.$el.find('#names-section')[0],
                    data: this.data,
                    dataKey: 'NAME.E41',
                    validateBranch: function (nodes) {
                        var valid = true;
                        var primaryname_count = 0;
                        var primaryname_conceptid = this.viewModel.primaryname_conceptid;
                        _.each(nodes, function (node) {
                            if (node.entitytypeid === 'NAME.E41') {
                                if (node.value === ''){
                                    valid = false;
                                }
                            }
                            if (node.entitytypeid === 'NAME_TYPE.E55') {
                                if (node.value === primaryname_conceptid){
                                    _.each(self.viewModel['branch_lists'], function (branch_list) {
                                        _.each(branch_list.nodes, function (node) {
                                            if (node.entitytypeid === 'NAME_TYPE.E55' && node.value === primaryname_conceptid) {
                                                valid = false;
                                            }
                                        }, this);
                                    }, this);
                                }
                            }
                        }, this);
                        return valid;
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#dates-section')[0],
                    data: this.data,
                    dataKey: 'important_dates',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    },
                    onSelect2Selecting: function(item, select2Config){
                        _.each(this.editedItem(), function(node){
                            if ('BEGINNING_OF_EXISTENCE_TYPE.E55,END_OF_EXISTENCE_TYPE.E55'.search(node.entitytypeid()) > -1){
                                node.label(item.value);
                                //node.value(item.id);
                                node.entitytypeid(item.entitytypeid);
                            }
                        }, this);
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#subjects-section')[0],
                    data: this.data,
                    dataKey: 'KEYWORD.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#heritage-type-section')[0],
                    data: this.data,
                    dataKey: 'RESOURCE_TYPE_CLASSIFICATION.E55',
                    alwaysEdit: true,
                    validateBranch: function (nodes) {
                        return true;
                    },
                    onSelect2Selecting: function(item, select2Config){
                        _.each(this.editedItem(), function(node){
                            if (node.entitytypeid() === select2Config.dataKey){
                                node.label(item.value);
                                //node.value(item.id);
                                node.entitytypeid(item.entitytypeid);
                            }
                        }, this);
                        this.trigger('change', 'changing', item);
                    }
                }));

            }
        });
    }
);