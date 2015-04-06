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
            var resourcetypeid = $('#resourcetypeid').val();
            var includeMap = (resourcetypeid !== 'ACTOR.E39');
            var includeSettings = !_.contains(['ACTOR.E39', 'ACTIVITY.E7', 'HERITAGE_RESOURCE_GROUP.E27', 'HISTORICAL_EVENT.E5'], resourcetypeid);
            var includeAdminAreas = (resourcetypeid !== 'ACTOR.E39');
            var includeParcels = !_.contains(['ACTOR.E39', 'ACTIVITY.E7', 'HISTORICAL_EVENT.E5'], resourcetypeid);

            BaseForm.prototype.initialize.apply(this);

            if (includeMap) {
                var map = new MapView({
                    el: $('#map')
                });

                var addFeature = function (feature, editing) {
                    var branch = koMapping.fromJS({
                        'editing': ko.observable(editing), 
                        'nodes': ko.observableArray(locationBranchList.defaults)
                    });
                    var geom = feature.getGeometry();
                    if (editing) {
                        locationBranchList.removeEditedBranch();
                    }
                    geom.transform(ol.proj.get('EPSG:3857'), ol.proj.get('EPSG:4326'));
                    _.each(branch.nodes(), function(node) {
                        if (node.entitytypeid() === 'SPATIAL_COORDINATES_GEOMETRY.E47') {
                            node.value(wkt.writeGeometry(geom));
                        }
                    });
                    locationBranchList.viewModel.branch_lists.push(branch);
                    self.trigger('change', 'geometrychange', branch);
                };

                var bulkAddFeatures = function (features) {
                    _.each(features, function(feature, i) {
                        addFeature(feature, i===features.length-1);
                    });
                    zoomToFeatureOverlay();
                };

                map.map.on('click', function(e) {
                    map.map.forEachFeatureAtPixel(e.pixel, function (feature, layer) {
                        if (_.contains(feature.getKeys(), 'branch')) {
                            locationBranchList.removeEditedBranch();
                            feature.get('branch').editing(true);            
                        }
                    });
                });

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

                var style = function (feature) {
                    var editing = feature.get('editing');
                    return [new ol.style.Style({
                        fill: new ol.style.Fill({
                            color: 'rgba(92, 184, 92, 0.5)'
                        }),
                        stroke: new ol.style.Stroke({
                            color: '#5cb85c',
                            width: editing ? 4 : 2
                        }),
                        image: new ol.style.Circle({
                            radius: editing ? 9 : 7,
                            fill: new ol.style.Fill({
                                color: 'rgba(92, 184, 92, 0.5)'
                            }),
                            stroke: new ol.style.Stroke({
                                color: '#5cb85c',
                                width: editing ? 4 : 2
                            })
                        })
                    })];
                }

                var featureOverlay = new ol.FeatureOverlay({
                    style: style
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
                            branch: branch,
                            editing: branch.editing()
                        });

                        branch.editing.subscribe(function () {
                            feature.set('editing', branch.editing());
                            map.map.render();
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
                        addFeature(e.feature, true);
                        map.map.removeInteraction(draw);
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