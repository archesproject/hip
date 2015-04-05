define(['jquery', 'views/forms/base', 'views/forms/sections/branch-list', ], function ($, BaseForm, BranchList) {
        return BaseForm.extend({
            initialize: function() {
                BaseForm.prototype.initialize.apply(this);                
                var self = this;

                this.addBranchList(new BranchList({
                    el: this.$el.find('#titles-section')[0],
                    data: this.data,
                    dataKey: 'TITLE.E41',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#identifiers-section')[0],
                    data: this.data,
                    dataKey: 'IDENTIFIER.E42',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));


                this.addBranchList(new BranchList({
                    el: this.$el.find('#formats-section')[0],
                    data: this.data,
                    dataKey: 'INFORMATION_CARRIER.E84',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#languages-section')[0],
                    data: this.data,
                    dataKey: 'LANGUAGE.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));

                this.addBranchList(new BranchList({
                    el: this.$el.find('#keywords-section')[0],
                    data: this.data,
                    dataKey: 'KEYWORD.E55',
                    validateBranch: function (nodes) {
                        return this.validateHasValues(nodes);
                    }
                }));
            }
        });
});


