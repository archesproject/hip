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
            var self = this;
            var resourcetypeid = $('#resourcetypeid').val();
            var includeMap = (resourcetypeid !== 'ACTOR.E39');
            var includeSettings = !_.contains(['ACTOR.E39', 'ACTIVITY.E7', 'HERITAGE_RESOURCE_GROUP.E27', 'HISTORICAL_EVENT.E5'], resourcetypeid);
            var includeAdminAreas = (resourcetypeid !== 'ACTOR.E39');
            var includeParcels = !_.contains(['ACTOR.E39', 'ACTIVITY.E7', 'HISTORICAL_EVENT.E5'], resourcetypeid);

            BaseForm.prototype.initialize.apply(this);

            if (includeMap) {
                this.addBranchList(new LocationBranchList({
                    el: this.$el.find('#geom-list-section')[0],
                    data: this.data,
                    dataKey: 'SPATIAL_COORDINATES_GEOMETRY.E47'
                }));
            }

            if (includeSettings) {
                this.addBranchList(new BranchList({
                    el: this.$el.find('#setting-section')[0],
                    data: this.data,
                    dataKey: 'SETTING_TYPE.E55'
                }));
            }

            if (includeAdminAreas) {
                this.addBranchList(new BranchList({
                    el: this.$el.find('#admin-area-section')[0],
                    data: this.data,
                    dataKey: 'ADMINISTRATIVE_SUBDIVISION.E48'
                }));
            }

            if (includeParcels) {
                this.addBranchList(new BranchList({
                    el: this.$el.find('#parcel-section')[0],
                    data: this.data,
                    dataKey: 'PLACE_APPELLATION_CADASTRAL_REFERENCE.E44'
                }));
            }

            this.addBranchList(new BranchList({
                el: this.$el.find('#address-section')[0],
                data: this.data,
                dataKey: 'PLACE_ADDRESS.E45'
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#description-section')[0],
                data: this.data,
                dataKey: 'DESCRIPTION_OF_LOCATION.E62',
                singleEdit: true
            }));
        }
    });
});