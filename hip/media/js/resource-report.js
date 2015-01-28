require([
    'jquery',
    'arches',
    'bootstrap',
    'views/map',
    'openlayers', 
    'knockout',
    'map/resource-layer-model'
], function($, arches, bootstrap, MapView, ol, ko, ResourceLayerModel) {
    var ReportView = Backbone.View.extend({

        initialize: function(options) { 
            var self = this;
            var resource_geometry = $('#resource_geometry');

            this.vectorLayer = new ResourceLayerModel().layer();
            this.map = new MapView({
                el: $('#map'),
                overlays: [this.vectorLayer]
            });

            ko.applyBindings(this.map, $('#basemaps-panel')[0]);

            this.highlightFeatures(JSON.parse(resource_geometry.val()));
            this.zoomToResource('1');

            var hideAllPanels = function(){
                $("#basemaps-panel").addClass("hidden");

                //Update state of remaining buttons
                $("#inventory-basemaps")
                    .removeClass("arches-map-tools-pressed")
                    .addClass("arches-map-tools")
                    .css("border-bottom-left-radius", "1px");
            };

            //Inventory-basemaps button opens basemap panel
            $("#inventory-basemaps").click(function (){
                if ($(this).hasClass('arches-map-tools-pressed')) {
                    hideAllPanels();
                } else {
                    $("#basemaps-panel").removeClass("hidden");

                    //Update state of current button and adjust position
                    $("#inventory-basemaps")
                        .addClass("arches-map-tools-pressed")
                        .removeClass("arches-map-tools")
                        .css("border-bottom-left-radius", "5px");
                }
            });

            $(".basemap").click(function (){ 
                var basemap = $(this).attr('id');
                _.each(self.map.baseLayers, function(baseLayer){ 
                    baseLayer.layer.setVisible(baseLayer.id == basemap);
                });
                hideAllPanels();
            });

            //Close Button
            $(".close").click(function (){ 
                hideAllPanels();
            });

        },

        zoomToResource: function(resourceid){
            this.cancelFitBaseLayer = true;
            var feature = this.selectedFeatureLayer.getSource().getFeatureById(resourceid);
            if(feature.getGeometry().getGeometries().length > 1){
                var extent = feature.getGeometry().getExtent();
                var minX = extent[0];
                var minY = extent[1];
                var maxX = extent[2];
                var maxY = extent[3];
                var polygon = new ol.geom.Polygon([[[minX, minY], [maxX, minY], [maxX, maxY], [minX, maxY], [minX, minY]]]);
                this.map.map.getView().fitGeometry(polygon, this.map.map.getSize(), {maxZoom:16}); 
            }else{
                this.map.map.getView().fitGeometry(feature.getGeometry().getGeometries()[0], this.map.map.getSize(), {maxZoom:16});                    
            }
        },

        hexToRgb: function (hex) {
            var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
            return result ? {
                r: parseInt(result[1], 16),
                g: parseInt(result[2], 16),
                b: parseInt(result[3], 16)
            } : null;
        },

        highlightFeatures: function(geometry){
            var source, geometries;
            var self = this;
            var f = new ol.format.GeoJSON({defaultDataProjection: 'EPSG:4326'});

            if(!this.selectedFeatureLayer){
                var rgb = this.hexToRgb('#C4171D');
                var iconUnicode = '\uf060';                    
                var zIndex = 0;
                var styleCache = {};

                var style = function(feature, resolution) {
                    var mouseOver = feature.get('mouseover');
                    var text = '1 ' + mouseOver;

                    feature.set('arches_marker', true);

                    if (styleCache[text]) {
                        return styleCache[text];
                    }
                    
                    var iconSize = mouseOver ? 38 : 32;

                    var styles = [new ol.style.Style({
                        text: new ol.style.Text({
                            text: iconUnicode,
                            font: 'normal ' + iconSize + 'px octicons',
                            offsetX: 5,
                            offsetY: ((iconSize/2)*-1)-5,
                            fill: new ol.style.Fill({
                                color: 'rgba(126,126,126,0.3)',
                            })
                        }),
                        zIndex: mouseOver ? zIndex*1000000000: zIndex
                    }), new ol.style.Style({
                        text: new ol.style.Text({
                            text: iconUnicode,
                            font: 'normal ' + iconSize + 'px octicons',
                            offsetY: (iconSize/2)*-1,
                            stroke: new ol.style.Stroke({
                                color: 'white',
                                width: 3
                            }),
                            fill: new ol.style.Fill({
                                color: 'rgba(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ',0.9)',
                            })
                        }),
                        zIndex: mouseOver ? zIndex*2000000000 : zIndex+1
                    })];

                    zIndex += 2;

                    styleCache[text] = styles;
                    return styles;
                };                     
                this.selectedFeatureLayer = new ol.layer.Vector({
                    source: new ol.source.GeoJSON(),
                    style: style
                });
                this.map.map.addLayer(this.selectedFeatureLayer);  
            }
            this.selectedFeatureLayer.getSource().clear();

            feature = {
                'type': 'Feature',
                'id': '1',
                'geometry':  geometry
            };

            this.selectedFeatureLayer.getSource().addFeature(f.readFeature(feature, {featureProjection: 'EPSG:3857'}));
        }
    });

    new ReportView();
});
