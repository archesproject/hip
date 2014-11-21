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


            this.NameModel = function(names) {
                this.names = ko.observableArray(names);   
            };

            // attach the view models to the dom elements
            this.nameViewModel = new this.NameModel(this.formdata.names);
            ko.applyBindings(this.nameViewModel, $('#names-form')[0]);
        },

        addName: function(data) {
            this.nameViewModel.names.push({
                id: '',
                name: $('#resource-name').val(),
                type_id: $('#resource-name-type').val(),
                type_name: $('#resource-name-type option:selected').text()
            });
        },

        deleteName: function(el) {
            var data = $(el.target).data();

            this.nameViewModel.names.remove(function(item) {
                return item.name === data.id;
            });
        },

        submit: function(){
            this.form.find('#formdata').val(ko.toJSON(this.nameViewModel));
            this.form.submit();
        }
    });
});