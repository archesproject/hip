define([
    'jquery',
    'openlayers',
    'underscore',
    'arches',
    'layer-info'
], function($, ol, _, arches, layerInfo) {
    var layers = [];

    _.each(layerInfo, function (item, entitytypeid) {
      var color = '#'+Math.floor(Math.random()*16777215).toString(16);

      var style = new ol.style.Style({
        fill: new ol.style.Fill({
          color: color
        }),
        stroke: new ol.style.Stroke({
          color: color,
          width: 1
        })
      });

      var source = new ol.source.GeoJSON({
        projection: 'EPSG:3857',
        url: 'resources/layers/' + entitytypeid + '/'
      });

      var layer = new ol.layer.Vector({
        source: source,
        style: style
      });

      var layerModel = _.extend({
        layer: layer,
        onMap: true
      }, layerInfo[entitytypeid]);

      layers.push(layerModel);
    });

    return layers;
});