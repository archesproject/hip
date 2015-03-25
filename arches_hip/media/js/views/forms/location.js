define([
    'jquery',
    'underscore',
    'openlayers',
    'views/forms/base',
    'views/forms/sections/branch-list',
    'views/map',
], function ($, _, ol, BaseForm, BranchList, MapView) {
    return BaseForm.extend({
        initialize: function() {
            BaseForm.prototype.initialize.apply(this);

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
            
            var map = new MapView({
                el: $('#map')
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

            
            var geometryType = 'Polygon';


            var draw;
            function addInteraction() {

              draw = new ol.interaction.Draw({
                features: featureOverlay.getFeatures(),
                type: geometryType //(typeSelect.value)
              });
              map.map.addInteraction(draw);

            }


            //Set up geometry selection tools.  
            $(".geometry").click(function (){ 
                
                geometryType = $(this).attr('id');
                map.map.removeInteraction(draw);
                addInteraction();

                //close panel
                $("#inventory-home").click();
                //$("#overlay-panel").addClass("hidden");

                //show geometry type selection
                //$("#geometry-type").removeClass("hidden");


                //keep page from re-loading
                return false;

            }); 
            $(".geometry").select('click');


            addInteraction();
        }
    });
});