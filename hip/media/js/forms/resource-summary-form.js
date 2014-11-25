define(['jquery', 'backbone', 'knockout', 'knockout-mapping', 'underscore', 'views/forms/base'], function ($, Backbone, ko, koMapping, _, BaseForm) {
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

            this.viewModel.editing.NAME_E41 = koMapping.fromJS(this.viewModel.defaults.NAME_E41);

            this.viewModel.editing.NAME_E41.NAME_TYPE_E55__value.subscribe(function(newValue) {
                self.viewModel.editing.NAME_E41.NAME_TYPE_E55__label($('#resource-name-type option:selected').text());
            });
        },

        addName: function(data) {
            var self = this;

            this.viewModel.NAME_E41.push(ko.toJS(this.viewModel.editing.NAME_E41));
            
            koMapping.fromJS(this.viewModel.defaults.NAME_E41, this.viewModel.editing.NAME_E41);
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