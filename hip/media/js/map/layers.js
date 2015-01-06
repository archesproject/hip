define([
    'map/resource-layers',
    'map/layer-model'
], function(resourceLayers, LayerModel) {
    var layers = resourceLayers.layers;
    layers.push(new LayerModel({
        name: 'Los Angeles Parcels',
        icon: 'fa fa-bookmark-o',
        layer: new ol.layer.Tile({
            source: new ol.source.XYZ({
                url: 'http://egis3.lacounty.gov/arcgis/rest/services/LACounty_Cache/LACounty_Parcel/MapServer/tile/{z}/{y}/{x}'
            })
        })
    }));
    return layers;
});