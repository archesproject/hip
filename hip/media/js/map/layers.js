define([
    'openlayers',
    'map/resource-layers',
    'map/layer-model'
], function(ol, resourceLayers, LayerModel) {
    var layers = resourceLayers.layers;
    var cityLimitFeature = {
        "type": "Feature",
        "properties": {},
    };

    layers.push(new LayerModel({
        name: 'Los Angeles City Limits',
        icon: 'fa fa-bookmark-o',
        visibleZoomRange: '9-20',
        onMap: true,
        layer: new ol.layer.Vector({
            style: new ol.style.Style({
                fill: new ol.style.Fill({
                	color: 'rgba(255,255,255,0.5)'
                }),
                stroke: new ol.style.Stroke({
                    color: '#555',
                    width: 1
                })
            }),
            source: new ol.source.GeoJSON({
                projection: 'EPSG:3857',
                object: {
                    'type': 'FeatureCollection',
                    'crs': {
                      'type': 'name',
                      'properties': {
                        'name': 'EPSG:4326'
                      }
                    },
                    'features': [cityLimitFeature]
                }
            })
        })
    }));

    layers.push(new LayerModel({
        name: 'Los Angeles Parcels',
        icon: 'fa fa-bookmark-o',
        visibleZoomRange: '15-20',
        layer: new ol.layer.Tile({
            source: new ol.source.XYZ({
                url: 'http://egis3.lacounty.gov/arcgis/rest/services/LACounty_Cache/LACounty_Parcel/MapServer/tile/{z}/{y}/{x}'
            })
        })
    }));

    return layers;
});