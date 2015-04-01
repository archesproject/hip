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
        initialize: function() {
            WizardBase.prototype.initialize.apply(this);

        }

    });
});