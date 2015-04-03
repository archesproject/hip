define(['jquery', 'underscore', 'knockout-mapping', 'views/forms/base', 'views/forms/sections/branch-list'], function ($, _, koMapping, BaseForm, BranchList) {
    return BaseForm.extend({
        initialize: function() {
            BaseForm.prototype.initialize.apply(this);

            var date_picker = $('.datetimepicker').datetimepicker({pickTime: false});
            date_picker.on('dp.change', function(evt){
                $(this).find('input').trigger('change'); 
            });

            this.addBranchList(new BranchList({
                el: this.$el.find('#name-section')[0],
                data: this.data,
                dataKey: 'APPELLATION.E41',
                validateBranch: function (nodes) {
                    var valid = true;
                    var primaryname_count = 0;
                    var primaryname_conceptid = this.viewModel.primaryname_conceptid;
                    _.each(nodes, function (node) {
                        if (node.entitytypeid === 'ACTOR_APPELLATION.E82') {
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
                el: this.$el.find('#epithet-section')[0],
                data: this.data,
                dataKey: 'EPITHET.E82',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#begin-date-section')[0],
                data: this.data,
                dataKey: 'BEGINNING_OF_EXISTENCE.E63',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#end-date-section')[0],
                data: this.data,
                dataKey: 'END_OF_EXISTENCE.E64',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#keyword-section')[0],
                data: this.data,
                dataKey: 'KEYWORD.E55',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
        }
    });
});

