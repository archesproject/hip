require(['jquery', 
    'underscore',
    'backbone',
    'bootstrap',
    'arches', 
    'views/resource-search', 
    'views/map',
    'openlayers', 
    'knockout',
    'plugins/bootstrap-slider/bootstrap-slider.min',
    'plugins/bootstrap-tags/bootstrap-tagsinput.min'], 
    function($, _, Backbone, bootstrap, arches, ResourceSearch, MapView, ol, ko, Slider, TagsInput) {
    $(document).ready(function() {

        var SearchResultsView = Backbone.View.extend({
            el: $('body'),
            updateRequest: '',
            mapExpanded: false,
            timeExpaned: false,
            pageChanged: false,

            events: {
                'click .page-button': 'newPage',
                'click #view-saved-searches': 'showSavedSearches',
                'click #map-filter-button': 'toggleMapFilter',
                'click #time-filter-button': 'toggleTimeFilter',
                'click .layer-zoom': 'layerZoom',
                'click #map-extent-filter': 'toggleSpatialFilter',
                'click #polygon-filter': 'toggleSpatialFilter',
                'click #point-filter': 'toggleSpatialFilter',
                'click #line-filter': 'toggleSpatialFilter',
                'click #spatial-buffer': 'toggleSpatialFilter',
                'click #map-tools-btn': 'handleMapToolsBtn'
            },

            initialize: function(options) { 
                var self = this;

                var initialcount = $('#search-results-count').data().count;

                $("#map-extent-filter-tag").removeClass('hidden');
                $(".bootstrap-tagsinput").css("border-width", "0px");

                this.temporalFilterViewModel = {
                    year_min_max: ko.observableArray(),
                    filters: ko.observableArray()
                };

                this.spatialFilterViewModel = {
                    type: ko.observable(''),
                    coordinates: ko.observable([])
                };

                ko.applyBindings(this.spatialFilterViewModel, $('#map-tools-btn')[0]); 

                this.searchQuery = {
                    page: ko.observable(),
                    q: ko.observableArray(),
                    date: this.temporalFilterViewModel,
                    spatialFilter: this.spatialFilterViewModel,
                    queryString: function(){
                        var params = {
                            page: this.page(),
                            q: ko.toJSON(this.q()),
                            year_min_max: ko.toJSON(this.date.year_min_max()),
                            spatialFilter: ko.toJSON(this.spatialFilter)
                        }; 
                        return $.param(params);
                    }, 
                    isEmpty: function(){
                        if (!(self.searchQuery.page()) && 
                            self.searchQuery.q().length === 0 && 
                            self.searchQuery.date.year_min_max.length === 0 && 
                            self.searchQuery.spatialFilter.type() === ''){
                            return true;
                        }
                        return false;
                    },
                    changed: ko.pureComputed(function(){
                        var ret = ko.toJSON(this.searchQuery.page()) +
                            ko.toJSON(this.searchQuery.q()) +
                            ko.toJSON(this.searchQuery.date.year_min_max()) +
                            ko.toJSON(this.searchQuery.spatialFilter.coordinates());
                        return ret;
                    }, this).extend({ rateLimit: 0 })
                }

                this.searchQuery.changed.subscribe(function(){
                    if(!self.pageChanged){
                        self.searchQuery.page(1);
                    }
                    self.updateResults();
                    self.pageChanged = false;
                });

                this.searchbox = new ResourceSearch({
                    el: $.find('input.resource_search_widget')[0]
                });

                this.searchbox.on('change', function(e, el){
                    if(e.added){
                        self.termFilterViewModel.filters.push(e.added);
                    }
                    if(e.removed){
                        self.termFilterViewModel.filters.remove(e.removed);
                    }
                    self.updateTermFilter();
                });

                this.searchRestulsViewModel = {
                    total: ko.observable(initialcount),
                    results: ko.observableArray()
                };
                ko.applyBindings(this.searchRestulsViewModel, $('#search-results-list')[0]);
                ko.applyBindings(this.searchRestulsViewModel, $('#search-results-count')[0]);

                this.searchRestulsViewModel.results.subscribe(function(resultsarray){
                    self.highlightFeatures(resultsarray);
                });

                this.termFilterViewModel = {
                    filters: ko.observableArray()
                };
                // this.termFilterViewModel.filters.subscribe(function(){
                //     console.log(arguments);
                // });
                //ko.applyBindings(this.termFilterViewModel, $('#map-filter')[0]);


                


                this.addResourceLayer();

                this.initTemporalFilter();

                this.getSearchQuery();

            },

            addResourceLayer: function(){

                var style = new ol.style.Style({
                    fill: new ol.style.Fill({
                        color: '#9E9E9E'
                    }),
                    stroke: new ol.style.Stroke({
                        color: '#9E9E9E',
                        width: 1
                    }),
                    image: new ol.style.Circle({
                        radius: 5,
                        stroke: new ol.style.Stroke({
                            color: '#fff'
                        }),
                        fill: new ol.style.Fill({
                            color: '#9E9E9E'
                        })
                    })
                });

                this.vectorLayer = new ol.layer.Vector({
                    //maxResolution: arches.mapDefaults.cluster_min,
                    source: new ol.source.GeoJSON({
                        projection: 'EPSG:3857',
                        url: 'resources/layers/'
                    }),
                    style: style
                });

                this.map = new MapView({
                    el: $('#map'),
                    overlays: [this.vectorLayer]
                });

                var highlightStyleCache = {};
                this.featureOverlay = new ol.FeatureOverlay({
                    map: this.map.map,
                    style: function(feature, resolution) {
                        var text = resolution < 5000 ? feature.get('primaryname') : '';
                        if (!highlightStyleCache[text]) {
                            highlightStyleCache[text] = [
                                new ol.style.Style({
                                    fill: new ol.style.Fill({
                                        color: '#00C819'
                                    }),
                                    stroke: new ol.style.Stroke({
                                        color: '#00C819',
                                        width: 1
                                    }),
                                    image: new ol.style.Circle({
                                        radius: 5,
                                        stroke: new ol.style.Stroke({
                                            color: '#fff'
                                        }),
                                        fill: new ol.style.Fill({
                                            color: '#00C819'
                                        })
                                    }),
                                    text: new ol.style.Text({
                                        font: '12px Calibri,sans-serif',
                                        text: text,
                                        offsetY: -12,
                                        fill: new ol.style.Fill({
                                            color: '#fff',
                                            width: 4
                                        }),
                                        stroke: new ol.style.Stroke({
                                            color: '#006E2B',
                                            width: 4
                                        })
                                    })
                                })
                            ];
                        }
                        return highlightStyleCache[text];
                    }
                });

                // var displayFeatureInfo = function(pixel) {

                //     var feature = map.forEachFeatureAtPixel(pixel, function(feature, layer) {
                //         return feature;
                //     });

                //     var info = document.getElementById('info');
                //     if (feature) {
                //         info.innerHTML = feature.getId() + ': ' + feature.get('name');
                //     } else {
                //         info.innerHTML = '&nbsp;';
                //     }

                // };

                // $(map.getViewport()).on('mousemove', function(evt) {
                //     var pixel = map.getEventPixel(evt.originalEvent);
                //     displayFeatureInfo(pixel);
                // });

                // map.on('click', function(evt) {
                //     displayFeatureInfo(evt.pixel);
                // });


                function zoomToLayer(vectorLayer, map){
                    var extent = (vectorLayer.getSource().getExtent());
                    var size = (map.map.getSize());
                    var view = map.map.getView()
                    view.fitExtent(
                        extent,
                        size
                    );
                }

                zoomToLayer(this.vectorLayer, this.map)

            },

            highlightFeatures: function(resultsarray){
                this.featureOverlay.getFeatures().clear();
                _.each(resultsarray, function(result){
                    var feature = this.vectorLayer.getSource().getFeatureById(result.resourceid);
                    if(feature){
                        this.featureOverlay.addFeature(feature);
                    }
                }, this);
            },

            getMapExtent: function(){
                var extent = ol.proj.transformExtent(this.map.map.getView().calculateExtent(this.map.map.getSize()), 'EPSG:3857', 'EPSG:4326');
                return extent;
            },

            onMoveEnd: function(evt) {
                this.spatialFilterViewModel.coordinates(this.getMapExtent());
            },

            toggleSpatialFilter: function(evt){
                var link = $(evt.target).closest('a');
                var data = link.data();
                var item = link.find('i');
                
                if (!(item.hasClass("fa-check"))){
                    //User is adding filter
                    //item.removeClass("fa-xxx").addClass("fa-check");

                    if(data.tooltype){
                        //Update filter tag
                        $(".bootstrap-tagsinput").css("display", "block");

                        if(data.tooltype === 'map-extent'){
                            this.spatialFilterViewModel.type('bbox');
                            this.spatialFilterViewModel.coordinates(this.getMapExtent());
                            this.map.map.on('moveend', this.onMoveEnd, this);
                        }else{
                            this.spatialFilterViewModel.type(data.tooltype);
                            this.enableDrawingTools(this.map.map, data.tooltype);
                            this.map.map.un('moveend', this.onMoveEnd, this);     
                        }                  
                    }

                }else{
                    //User is removing filter
                    //item.removeClass("fa-check").addClass("fa-xxx");

                    if(data.tooltype){
                        //Update filter tag
                        $(".bootstrap-tagsinput").css("display", "none");

                        this.spatialFilterViewModel.type('');
                        this.spatialFilterViewModel.coordinates([]);

                        if(data.tooltype === 'map-extent'){
                            this.map.map.un('moveend', this.onMoveEnd, this);
                        } 

                        if(this.drawingtool){
                            this.map.map.removeInteraction(this.drawingtool);
                            this.drawingFeatureOverlay.getFeatures().clear();
                        }
                    }
                }
            },

            enableDrawingTools: function(map, tooltype){
                // The features are not added to a regular vector layer/source,
                // but to a feature overlay which holds a collection of features.
                // This collection is passed to the modify and also the draw
                // interaction, so that both can add or modify features.
                this.drawingFeatureOverlay = new ol.FeatureOverlay({
                    style: new ol.style.Style({
                        fill: new ol.style.Fill({
                            color: 'rgba(255, 255, 255, 0.2)'
                        }),
                        stroke: new ol.style.Stroke({
                            color: '#ffcc33',
                            width: 2
                        }),
                        image: new ol.style.Circle({
                            radius: 7,
                            fill: new ol.style.Fill({
                                color: '#ffcc33'
                            })
                        })
                    })
                });
                this.drawingFeatureOverlay.setMap(map);

                var modify = new ol.interaction.Modify({
                    features: this.drawingFeatureOverlay.getFeatures(),
                    // the SHIFT key must be pressed to delete vertices, so
                    // that new vertices can be drawn at the same position
                    // of existing vertices
                    deleteCondition: function(event) {
                        return ol.events.condition.shiftKeyOnly(event) &&
                                ol.events.condition.singleClick(event);
                    }
                });
                map.addInteraction(modify);

                if(this.drawingtool){
                    map.removeInteraction(this.drawingtool);
                }
                this.drawingtool = new ol.interaction.Draw({
                    features: this.drawingFeatureOverlay.getFeatures(),
                    type: tooltype
                });

                this.drawingtool.on('drawstart', function(){
                    this.drawingFeatureOverlay.getFeatures().clear();
                }, this);
                this.drawingtool.on('drawend', function(evt){
                    var geometry = evt.feature.getGeometry().clone();
                    geometry.transform('EPSG:3857', 'EPSG:4326');
                    this.spatialFilterViewModel.coordinates(geometry.getCoordinates());
                }, this);

                map.addInteraction(this.drawingtool);

            },

            initTemporalFilter: function(){
                var self = this;

                this.slider = new Slider('input.slider', {});
                this.slider.on('slideStop', function(evt){
                    // if ther user has the slider at it's min and max, then essentially they don't want to filter by year
                    if(self.slider.getAttribute('min') === evt.value[0] && self.slider.getAttribute('max') === evt.value[1]){
                        self.temporalFilterViewModel.year_min_max([]);
                    }else{
                        self.temporalFilterViewModel.year_min_max(evt.value);
                    }
                });

                this.temporalFilterViewModel.year_min_max.subscribe(function(newValue){
                    self.slider.setValue(newValue);
                });

                ko.applyBindings(this.temporalFilterViewModel, $('#time-filter')[0]);
            },

            newPage: function(evt){
                var data = $(evt.target).data();
                this.pageChanged = true;                
                this.searchQuery.page(data.page);
            },

            updateResults: function () {
                var self = this;
                if (this.updateRequest) {
                    this.updateRequest.abort();
                }
                this.updateRequest = $.ajax({
                    type: "GET",
                    url: arches.urls.search_results,
                    data: this.searchQuery.queryString(),
                    success: function(results){
                        $('#paginator').html(results);
                        self.bind(results);
                        self.toggleSearchResults('show');
                        self.toggleSavedSearches('hide');
                    },
                    error: function(){}
                });
            },

            bind: function(results){
                var self = this;
                var data = $('div[name="search-result-data"]').data();
                
                this.searchRestulsViewModel.total(data.results.hits.total);
                self.searchRestulsViewModel.results.removeAll();
                
                $.each(data.results.hits.hits, function(){
                    self.searchRestulsViewModel.results.push({
                        primaryname: this._source.primaryname,
                        resourceid: this._source.entityid,
                        entitytypeid: this._source.entitytypeid,
                        descritption: '',
                        geometries: ko.observableArray(this._source.geometries)
                    });
                });
            },

            showSavedSearches: function(){
                this.toggleSavedSearches('show');
                this.toggleSearchResults('hide');
            },

            hideSavedSearches: function(){
                this.toggleSavedSearches('hide');
                this.toggleSearchResults('show');
            },

            toggleSavedSearches: function(showOrHide){
                var ele = $('#saved-searches');
                this.slideToggle(ele, showOrHide);
            },

            toggleSearchResults: function(showOrHide){
                var ele = $('#search-results');
                this.slideToggle(ele, showOrHide);
            },

            toggleMapFilter: function(showOrHide){
                var ele = $('#map-filter');
                this.mapExpanded = this.toggleFilterSection(ele, this.mapExpanded)
            },

            toggleTimeFilter: function(showOrHide){
                var ele = $('#time-filter');
                this.timeExpaned = this.toggleFilterSection(ele, this.timeExpaned)
            },

            toggleFilterSection: function(ele, currentlyExpanded){
                if(!currentlyExpanded){
                    if(this.searchQuery.isEmpty()){
                        this.searchQuery.page(1);
                        this.slideToggle(ele, 'show');
                    }else{
                        
                        this.slideToggle(ele, 'show');
                        this.hideSavedSearches();
                    }
                }else{
                    this.slideToggle(ele, 'hide');               
                }
                return !currentlyExpanded;
            },

            slideToggle: function(ele, showOrHide){
                var self = this;
                if ($(ele).is(":visible") && showOrHide === 'hide'){
                    ele.slideToggle('slow');
                    return;
                }

                if (!($(ele).is(":visible")) && showOrHide === 'show'){
                    ele.slideToggle('slow', function(){
                        self.map.map.updateSize();
                    });
                    return;
                }

                if (!showOrHide){
                    ele.slideToggle('slow');                    
                }
            },

            updateTermFilter: function(){
                this.searchQuery.q(this.termFilterViewModel.filters());
            },

            setMapFilter: function(query){
                
            },

            setTimeFilter: function(query){
                
            },

            getSearchQuery: function(){
                var query = _.chain( location.search.slice(1).split('&') )
                    // Split each array item into [key, value]
                    // ignore empty string if search is empty
                    .map(function(item) { if (item) return item.split('='); })
                    // Remove undefined in the case the search is empty
                    .compact()
                    // Turn [key, value] arrays into object parameters
                    .object()
                    // Return the value of the chain operation
                    .value();

                if(query.page){
                    this.searchQuery.page(query.page);
                }
                if(query.q){
                    this.searchQuery.q(query.q);
                }
                if(query.date){
                    this.searchQuery.date(query.date);
                }
                if(query.spatialFilter){
                    this.searchQuery.spatialFilter(query.spatialFilter);
                }
                

                window.onpopstate = function(event) {
                  //alert("location: " + document.location + ", state: " + JSON.stringify(event.state));
                    //window.location = document.location;
                };
            },

            handleMapToolsBtn: function(evt){
                evt.stopPropagation();
            }


        });
        k = ko;
        x = new SearchResultsView();

    });
});