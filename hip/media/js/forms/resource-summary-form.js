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

            this.viewModel.names = ko.observableArray(self.formdata.names);
        },

        addName: function(data) {
            this.viewModel.names.push({
                id: '',
                name: $('#resource-name').val(),
                type_id: $('#resource-name-type').val(),
                type_name: $('#resource-name-type option:selected').text()
            });
        },

        deleteName: function(el) {
            var data = $(el.target).data();

            this.viewModel.names.remove(function(item) {
                return item.name === data.id;
            });
        },

        validate: function(){
            return true;
        }
    });
});