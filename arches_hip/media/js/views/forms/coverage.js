define([
    'jquery',
    'underscore',
    'views/forms/base',
    'views/forms/sections/branch-list',
    'views/forms/sections/location-branch-list',
    'summernote'
], function ($, _, BaseForm, BranchList, LocationBranchList) {
    return BaseForm.extend({
        initialize: function() {
            BaseForm.prototype.initialize.apply(this);

            this.addBranchList(new LocationBranchList({
                el: this.$el.find('#geom-list-section')[0],
                data: this.data,
                dataKey: 'SPATIAL_COORDINATES_GEOMETRY.E47'
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#description-section')[0],
                data: this.data,
                dataKey: 'DESCRIPTION_OF_LOCATION.E62',
                singleEdit: true
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#temporal-section')[0],
                data: this.data,
                dataKey: 'TEMPORAL_COVERAGE_TIME-SPAN.E52',
                singleEdit: true
            }));
        }
    });
});