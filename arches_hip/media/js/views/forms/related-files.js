define(['jquery', 
    'underscore', 
    'knockout',
    'views/forms/wizard-base', 
    'views/forms/sections/branch-list',
    'arches',
    'dropzone',
    'blueimp-gallery',
    'blueimp-jquery',
    'plugins/bootstrap-image-gallery.min'], function ($, _, ko, WizardBase, BranchList, arches, dropzone) {

    return WizardBase.extend({
        relatedfiles: ko.observableArray(),

        initialize: function() {
            WizardBase.prototype.initialize.apply(this);
            cc = this;
            k = ko;
            var self = this;
            var newfiles;
            var dropzoneEl = this.$el.find('.dropzone');   

            //ko.applyBindings(this, this.$el.find('#existing-assessments')[0]);  
            ko.applyBindings(this.relatedfiles, this.$el.find('#new-files-section')[0]);  


            // detect if dropzone is attached, and if not init
            if (!dropzoneEl.hasClass('dz-clickable')) {
                this.dropzoneInstance = new dropzone(dropzoneEl[0], {
                    url: arches.urls.concept,
                    acceptedFiles: 'image/*',
                    addRemoveLinks: true,
                    autoProcessQueue: false
                });

                this.dropzoneInstance.on("addedfile", function(file) {
                    var el = self.el.appendChild(this.hiddenFileInput);
                    var id = _.uniqueId('file_');
                    file.id = id;
                    el.setAttribute('name', id);
                    self.relatedfiles.push({
                        el: el,
                        id: id,
                        file: file,
                        title: ko.observable(),
                        description: ko.observable(),
                        relationshiptype: ko.observable(),
                        thumbnail: ko.observable(),
                        domains: self.data['current-files'].domains
                    })
                    this.hiddenFileInput = false;
                });

                this.dropzoneInstance.on("removedfile", function(filetoremove) {
                    var index;
                    _.each(self.relatedfiles(), function(file, i){
                        if (file.id === filetoremove.id){
                            index = i;
                        }
                    }, this);

                    self.el.removeChild(self.relatedfiles()[index].el);
                    self.relatedfiles.splice(index, 1);
                });

                this.dropzoneInstance.on("thumbnail", function(addedfile, thumbnaildata) {
                    _.each(self.relatedfiles(), function(file, i){
                        if (file.id === addedfile.id){
                            file.thumbnail(thumbnaildata);
                        }
                    }, this);
                });
            }

            this.addBranchList(new BranchList({
                el: this.$el.find('#current-files-section')[0],
                data: this.data,
                dataKey: 'current-files',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));
            

            this.newfilebranchlist = this.addBranchList(new BranchList({
                //el: this.$el.find('#new-files-section')[0],
                data: {'new-files':{'branch_lists': [], domains: this.data['current-files'].domains}},
                dataKey: 'new-files',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                },
                getData: function(){
                    var data = [];
                    _.each(self.relatedfiles(), function(item){
                        delete item.el;
                        delete item.file;
                        delete item.thumbnail;
                        delete item.domains;
                        data.push(item);
                    }, this); 
                    return data
                }
            }));
        }

    });
});