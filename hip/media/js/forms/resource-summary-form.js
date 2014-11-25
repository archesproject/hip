define(['jquery', 'backbone', 'knockout', 'views/forms/base'], function ($, Backbone, ko, BaseForm) {
    return BaseForm.extend({

        events: function(){
            return _.extend(BaseForm.prototype.events.apply(this), {
                'click #add-name-button': 'addName',
                'click .arches-CRUD-delete ': 'deleteName'
            }) 
        },

        initialize: function() {
            BaseForm.prototype.initialize.apply(this);

            this.$el.find('.resource-type').select2({
                placeholder: "type"
            });

            this.$el.find('.name-type').select2({
                placeholder: "name"
            });
            
            this.viewModel.NAME_E41 = ko.observableArray(this.viewModel.NAME_E41);
        },

        addName: function(data) {
            this.viewModel.NAME_E41.push({
                'NAME_E41_entityid': '',
                'NAME_E41_value': $('#resource-name').val(),
                'NAME_TYPE_E55_entityid': '',
                'NAME_TYPE_E55_value': $('#resource-name-type').val(),
                'NAME_TYPE_E55_label': $('#resource-name-type option:selected').text()
            });
        },

        deleteName: function(el) {
            var data = $(el.target).data();

            this.viewModel.NAME_E41.remove(function(item) {
                return item.NAME_E41_value === data.name_e41_value;
            });
        },

        validate: function(){
            return true;
        }
    });
});