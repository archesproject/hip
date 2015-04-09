define(['jquery', 
    'underscore', 
    'knockout',
    'knockout-mapping',
    'views/forms/wizard-base', 
    'views/forms/sections/branch-list',
    'arches',
    'dropzone',
    'blueimp-gallery',
    'blueimp-jquery',
    ], function ($, _, ko, koMapping, WizardBase, BranchList, arches, dropzone, Gallery) {

    return WizardBase.extend({

        initialize: function() {
            WizardBase.prototype.initialize.apply(this);

            var self = this;
            var dropzoneEl = this.$el.find('.dropzone'); 
            this.newfiles = ko.observableArray();  

            ko.applyBindings(this.newfiles, this.$el.find('#new-files-section')[0]);  

            // detect if dropzone is attached, and if not init
            if (!dropzoneEl.hasClass('dz-clickable')) {
                this.dropzoneInstance = new dropzone(dropzoneEl[0], {
                    url: arches.urls.concept,
                    acceptedFiles: 'image/*, application/pdf, text/*, .doc, .docx',
                    addRemoveLinks: true,
                    autoProcessQueue: false
                });

                this.dropzoneInstance.on("addedfile", function(file) {
                    var el = self.el.appendChild(this.hiddenFileInput);
                    var id = _.uniqueId('file_');
                    file.id = id;
                    el.setAttribute('name', id);
                    self.newfiles.push({
                        el: el,
                        id: id,
                        file: file,
                        title: ko.observable(file.name.split('.')[0]),
                        description: ko.observable(),
                        relationshiptype: ko.observable(),
                        thumbnail: ko.observable(),
                        domains: self.data['current-files'].domains
                    })
                    this.hiddenFileInput = false;
                });

                this.dropzoneInstance.on("removedfile", function(filetoremove) {
                    var index;
                    _.each(self.newfiles(), function(file, i){
                        if (file.id === filetoremove.id){
                            index = i;
                        }
                    }, this);

                    self.el.removeChild(self.newfiles()[index].el);
                    self.newfiles.splice(index, 1);
                });

                this.dropzoneInstance.on("thumbnail", function(addedfile, thumbnaildata) {
                    _.each(self.newfiles(), function(file, i){
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
                editor: {
                    'nodes': ko.observableArray(), 
                    'relationship': koMapping.fromJS({'relationshiptype': null}),
                    'domains': this.data['current-files'].domains
                },                
                validateBranch: function (nodes) {
                    return true;
                },
                editItem: function(model){
                    var modaldialog = $('#EditFileResourceModal');
                    modaldialog.modal().show();

                    this.editor.model = model;
                    this.editor.nodes.removeAll();
                    koMapping.fromJS(model.relationship, this.editor.relationship);
                    _.each(model.nodes(), function(node){
                        this.editor.nodes.push(node);
                    }, this);

                    $('#deletewarning').slideUp();
                    $('#editform').slideDown();
                    $('#savebtn').show();
                    $('#deletebtn').hide();
                },
                updateItem: function(branchlist, evt){
                    var data = koMapping.toJS(this.editor);
                    data.relationship.relationshiptype = data.relationship.relationshiptype.value;
                    delete data.domains;
                    
                    evt.preventDefault();

                    self.form.find('#formdata').val(JSON.stringify({'current-files': data}));
                    self.form.submit();
                },
                confirmDelete: function(branchlist, evt){
                    $('#deletewarning').slideDown(500);
                    $('#editform').slideUp(500);
                    $('#savebtn').hide(500);
                    $('#deletebtn').show(500);
                },
                deleteItem: function(branchlist, evt){
                    var relationship = koMapping.toJS(branchlist.editor).relationship;
                    relationship.relationshiptype = relationship.relationshiptype.value;

                    $.ajax({
                        url: arches.urls.related_resources + relationship.entityid1,
                        method: 'DELETE',
                        data: JSON.stringify(relationship),
                        success: function(response) {
                            branchlist.viewModel.branch_lists.remove(branchlist.editor.model);
                        }
                    });
                },
                getData: function(){
                    return [];
                }
            }));

            this.newfilebranchlist = this.addBranchList(new BranchList({
                //el: this.$el.find('#new-files-section')[0],
                data: {'new-files':{'branch_lists': [], domains: this.data['current-files'].domains}},
                dataKey: 'new-files',
                validate: function(){
                    var valid = true;
                    _.each(self.newfiles(), function(item){
                        if (item.title() == undefined || item.title() == '' || item.relationshiptype() == undefined || item.relationshiptype() == ''){
                            valid = false;
                        }
                    }, this); 
                    return valid;
                },
                getData: function(){
                    var data = [];
                    _.each(self.newfiles(), function(item){
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