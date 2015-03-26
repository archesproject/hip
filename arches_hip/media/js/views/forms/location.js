define([
    'jquery',
    'underscore',
    'knockout',
    'openlayers',
    'views/forms/base',
    'views/forms/sections/branch-list',
    'views/map',
    'summernote'
], function ($, _, ko, ol, BaseForm, BranchList, MapView) {
    return BaseForm.extend({
        initialize: function() {
            BaseForm.prototype.initialize.apply(this);

            var map = new MapView({
                el: $('#map')
            });

            var locationBranchList = new BranchList({
                el: this.$el.find('#geom-list-section')[0],
                data: this.data,
                dataKey: 'SPATIAL_COORDINATES_GEOMETRY.E47',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                },
                baseLayers: map.baseLayers
            });

            this.addBranchList(locationBranchList);

            this.addBranchList(new BranchList({
                el: this.$el.find('#address-section')[0],
                data: this.data,
                dataKey: 'PLACE_ADDRESS.E45',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#description-section')[0],
                data: this.data,
                dataKey: 'DESCRIPTION_OF_LOCATION.E62',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#setting-section')[0],
                data: this.data,
                dataKey: 'SETTING_TYPE.E55',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#admin-area-section')[0],
                data: this.data,
                dataKey: 'ADMINISTRATIVE_SUBDIVISION.E48',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#parcel-section')[0],
                data: this.data,
                dataKey: 'PLACE_APPELLATION_CADASTRAL_REFERENCE.E44',
                validateBranch: function (nodes) {
                    return this.validateHasValues(nodes);
                }
            }));

            var featureOverlay = new ol.FeatureOverlay({
              style: new ol.style.Style({
                fill: new ol.style.Fill({
                  color: 'rgba(92, 184, 92, 0.5)'
                }),
                stroke: new ol.style.Stroke({
                  color: '#5cb85c',
                  width: 2
                }),
                image: new ol.style.Circle({
                  radius: 7,
                  fill: new ol.style.Fill({
                    color: 'rgba(92, 184, 92, 0.5)'
                  }),
                  stroke: new ol.style.Stroke({
                    color: '#5cb85c',
                    width: 2
                  })
                })
              })
            });
            
            $("#inventory-home").click(function (){ 
                $("#overlay-panel").addClass("hidden");
                $("#basemaps-panel").addClass("hidden");

                $("#inventory-basemaps").removeClass("arches-map-tools-pressed");
                $("#inventory-basemaps").addClass("arches-map-tools");

                $("#inventory-overlays").removeClass("arches-map-tools-pressed");
                $("#inventory-overlays").addClass("arches-map-tools");


                $("#inventory-home").addClass("arches-map-tools-pressed");
                $("#inventory-home").removeClass("arches-map-tools");
                
                return false;
            });
            $("#inventory-basemaps").click(function (){ 
                $("#overlay-panel").addClass("hidden");
                $("#basemaps-panel").removeClass("hidden");

                $("#inventory-home").removeClass("arches-map-tools-pressed");
                $("#inventory-home").addClass("arches-map-tools");

                $("#inventory-overlays").removeClass("arches-map-tools-pressed");
                $("#inventory-overlays").addClass("arches-map-tools");

                $("#inventory-basemaps").addClass("arches-map-tools-pressed");
                $("#inventory-basemaps").removeClass("arches-map-tools");
                
                return false;
            });

            $("#inventory-overlays").click(function (){ 
                $("#overlay-panel").removeClass("hidden");
                $("#basemaps-panel").addClass("hidden");

                $("#inventory-home").removeClass("arches-map-tools-pressed");
                $("#inventory-home").addClass("arches-map-tools");

                $("#inventory-basemaps").removeClass("arches-map-tools-pressed");
                $("#inventory-basemaps").addClass("arches-map-tools");

                $("#inventory-overlays").addClass("arches-map-tools-pressed");
                $("#inventory-overlays").removeClass("arches-map-tools");

                return false;
            });

            featureOverlay.setMap(map.map);

            var modify = new ol.interaction.Modify({
              features: featureOverlay.getFeatures(),
              deleteCondition: function(event) {
                return ol.events.condition.shiftKeyOnly(event) &&
                    ol.events.condition.singleClick(event);
              }
            });
            map.map.addInteraction(modify);
        }
    });
});