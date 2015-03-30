define([
    'jquery',
    'underscore',
    'knockout',
    'knockout-mapping', 
    'openlayers',
    'views/forms/base',
    'views/forms/sections/branch-list',
    'views/map',
    'summernote'
], function ($, _, ko, koMapping, ol, BaseForm, BranchList, MapView) {
    var wkt = new ol.format.WKT();
    return BaseForm.extend({
        initialize: function() {
            var self = this;
            BaseForm.prototype.initialize.apply(this);

            var map = new MapView({
                el: $('#map')
            });

            var bulkAddFeatures = function (features) {
                locationBranchList.removeEditedBranch();
                _.each(features, function(feature, i) {
                    var branch = koMapping.fromJS({
                        'editing':ko.observable(i===features.length-1),
                        'nodes': ko.observableArray(locationBranchList.defaults)
                    });
                    var geom = feature.getGeometry();
                    geom.transform(ol.proj.get('EPSG:3857'), ol.proj.get('EPSG:4326'));
                    _.each(branch.nodes(), function(node) {
                        if (node.entitytypeid() === 'SPATIAL_COORDINATES_GEOMETRY.E47') {
                            node.value(wkt.writeGeometry(geom));
                        }
                    });
                    locationBranchList.viewModel.branch_lists.push(branch);
                });

                self.trigger('change', 'geometrychange');
                zoomToFeatureOverlay();
            };

            map.on('layerDropped', function (layer) {
                var features = layer.getSource().getFeatures();

                bulkAddFeatures(features);

                map.map.removeLayer(layer);
            });

            var getGeomNode = function (branch) {
                var geomNode = null;
                _.each(branch.nodes(), function(node) {
                    if (node.entitytypeid() === 'SPATIAL_COORDINATES_GEOMETRY.E47') {
                        geomNode = node;
                    }
                });
                return geomNode;
            };

            var locationBranchList = new BranchList({
                el: this.$el.find('#geom-list-section')[0],
                data: this.data,
                dataKey: 'SPATIAL_COORDINATES_GEOMETRY.E47',
                getBranchLists: function() {    
                    var branch_lists = [];
                    _.each(this.viewModel.branch_lists(), function(list){
                        _.each(list.nodes(), function(node) {
                            if (node.entitytypeid() === 'SPATIAL_COORDINATES_GEOMETRY.E47' && node.value() !== '') {
                                branch_lists.push(list);
                            }
                        });
                    }, this);
                    return branch_lists;
                },
                removeEditedBranch: function(){
                    var branch = this.getEditedBranch();
                    if (branch) {
                        branch.editing(false);
                    }
                    return branch;
                },
                baseLayers: map.baseLayers
            });

            locationBranchList.addDefaultNode('SPATIAL_COORDINATES_GEOMETRY.E47', '')

            this.addBranchList(locationBranchList);

            this.addBranchList(new BranchList({
                el: this.$el.find('#address-section')[0],
                data: this.data,
                dataKey: 'PLACE_ADDRESS.E45'
            }));

            var descriptionBranchList = new BranchList({
                el: this.$el.find('#description-section')[0],
                data: this.data,
                dataKey: 'DESCRIPTION_OF_LOCATION.E62',
                singleEdit: true
            });

            this.addBranchList(descriptionBranchList);

            this.addBranchList(new BranchList({
                el: this.$el.find('#setting-section')[0],
                data: this.data,
                dataKey: 'SETTING_TYPE.E55'
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#admin-area-section')[0],
                data: this.data,
                dataKey: 'ADMINISTRATIVE_SUBDIVISION.E48'
            }));

            this.addBranchList(new BranchList({
                el: this.$el.find('#parcel-section')[0],
                data: this.data,
                dataKey: 'PLACE_APPELLATION_CADASTRAL_REFERENCE.E44'
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

            var zoomToFeatureOverlay = function () {
                var extent = null;
                _.each(featureOverlay.getFeatures().getArray(), function(feature) {
                    var featureExtent = feature.getGeometry().getExtent();
                    if (!extent) {
                        extent = featureExtent;
                    } else {
                        extent = ol.extent.extend(extent, featureExtent);
                    }
                });

                if (extent) {
                    map.map.getView().fitExtent(extent, (map.map.getSize()));
                }
            }

            var refreshFreatureOverlay = function () {
                featureOverlay.getFeatures().clear();
                _.each(locationBranchList.getBranchLists(), function(branch) {
                    var geom = wkt.readGeometry(getGeomNode(branch).value());
                    geom.transform(ol.proj.get('EPSG:4326'), ol.proj.get('EPSG:3857'));
                    var feature = new ol.Feature({
                        geometry: geom,
                        branch: branch
                    });

                    feature.on('change', function () {
                        var cloneFeature = feature.clone();
                        var geom = cloneFeature.getGeometry();
                        geom.transform(ol.proj.get('EPSG:3857'), ol.proj.get('EPSG:4326'));
                        getGeomNode(branch).value(wkt.writeGeometry(geom));
                        locationBranchList.removeEditedBranch();
                        branch.editing(true);
                        self.trigger('change', 'geometrychange', branch);
                    });

                    featureOverlay.addFeature(feature);
                });
            }

            locationBranchList.viewModel.branch_lists.subscribe(refreshFreatureOverlay);
            refreshFreatureOverlay();
            zoomToFeatureOverlay();

            var draw = null;
            
            $(".geometry-btn").click(function (){ 
                var geometryType = $(this).data('geometrytype');
                if (draw) {
                    map.map.removeInteraction(draw);
                }
                draw = new ol.interaction.Draw({
                    features: featureOverlay.getFeatures(),
                    type: geometryType
                });
                draw.on('drawend', function(e) {
                    locationBranchList.removeEditedBranch();
                    var branch = koMapping.fromJS({
                        'editing':ko.observable(true), 
                        'nodes': ko.observableArray(locationBranchList.defaults)
                    });
                    var geom = e.feature.getGeometry();
                    geom.transform(ol.proj.get('EPSG:3857'), ol.proj.get('EPSG:4326'));
                    _.each(branch.nodes(), function(node) {
                        if (node.entitytypeid() === 'SPATIAL_COORDINATES_GEOMETRY.E47') {
                            node.value(wkt.writeGeometry(geom));
                        }
                    });
                    locationBranchList.viewModel.branch_lists.push(branch);
                    map.map.removeInteraction(draw);
                    self.trigger('change', 'geometrychange', branch);
                });
                map.map.addInteraction(draw);

                $("#inventory-home").click();
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

            $(".close").click(function (){ 
                $("#inventory-home").click()
            });

            var formatConstructors = [
                ol.format.GPX,
                ol.format.GeoJSON,
                ol.format.KML
            ];

            $('.geom-upload').on('change', function() {
                if (this.files.length > 0) {
                    var file = this.files[0];
                    var reader = new FileReader();
                    reader.onloadend = function(e) { 
                        var features = [];
                        var result = this.result;
                        _.each(formatConstructors, function(formatConstructor) {
                            var format = new formatConstructor();
                            var readFeatures;
                            try {
                                readFeatures = format.readFeatures(result);
                            } catch (e) {
                                readFeatures = null;
                            }
                            if (readFeatures !== null) {
                                _.each(readFeatures, function (feature) {
                                    var featureProjection = format.readProjection(result);
                                    var transform = ol.proj.getTransform(featureProjection, ol.proj.get('EPSG:3857'));
                                    var geometry = feature.getGeometry();
                                    if (geometry) {
                                        geometry.applyTransform(transform);
                                    }
                                    features.push(feature);
                                });
                            }
                        });
                        if (features.length > 0) {
                            bulkAddFeatures(features);
                        }
                    };
                    reader.readAsText(file);
                }
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