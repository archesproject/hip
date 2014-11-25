define(['jquery', 'backbone', 'knockout', 'underscore', 'views/forms/base'], function ($, Backbone, ko, _, BaseForm) {
    return BaseForm.extend({

        events: function(){
            return _.extend(BaseForm.prototype.events.apply(this), {
                'click #add-name-button': 'addName',
                'click .arches-CRUD-delete ': 'deleteName'
            }) 
        },

        initialize: function() {
            var self = this;

            BaseForm.prototype.initialize.apply(this);

            this.$el.find('.resource-type, .name-type').select2();

            this.viewModel.NAME_E41 = ko.observableArray(this.viewModel.NAME_E41);

            this.viewModel._defaults.NAME_E41 = {
                'NAME_E41__entityid': '',
                'NAME_E41__value': '',
                'NAME_TYPE_E55__entityid': '',
                'NAME_TYPE_E55__value': $('#resource-name-type').val(),
                'NAME_TYPE_E55__label': $('#resource-name-type option:selected').text()
            }

            this.viewModel._editing.NAME_E41 = _.clone(this.viewModel._defaults.NAME_E41);
            
            _.map(this.viewModel._editing.NAME_E41, function(val, key){
                self.viewModel._editing.NAME_E41[key] = ko.observable(val);
            });

            this.viewModel._editing.NAME_E41.NAME_TYPE_E55__value.subscribe(function(newValue) {
                self.viewModel._editing.NAME_E41.NAME_TYPE_E55__label($('#resource-name-type option:selected').text());
            });
        },

        addName: function(data) {
            var self = this;

            this.viewModel.NAME_E41.push(ko.toJS(this.viewModel._editing.NAME_E41));
            
            _.map(this.viewModel._editing.NAME_E41, function(val, key){
                self.viewModel._editing.NAME_E41[key](self.viewModel._defaults.NAME_E41[key]);
            });
        },

        deleteName: function(el) {
            var data = $(el.target).data();

            this.viewModel.NAME_E41.remove(function(item) {
                return item.NAME_E41__value === data.name_e41__value;
            });
        },

        validate: function(){
            return true;
        }
    });
});