require(['jquery','arches','bootstrap','openlayers'], function($, arches) {
    $(document).ready(function() {
        //ContactPage.initMap();
        CirclesMaster.initCirclesMaster1();
    
        //Add Report Options Button to Listen
        var el = document.getElementById("report_options");
        
        //On Report Options Button Click, run handleArchesReport
        if (el.addEventListener)
            el.addEventListener("click", handleArchesReport, false);
        else if (el.attachEvent)
            el.attachEvent('onclick', handleArchesReport);

        function handleArchesReport() {    
            var panel = $('.arches-report-options');
            //get position of the Report options button, and use to place the panel
            //relative to the button
            var offset = $("#report_options").offset().top + $("#report_options").height();
            var left_edge = parseInt($("#report_options").offset().left);
            
            //OK, the right edge of the panel can now be calculated as follows:
            //find the right edge of the button, and add the button width to find the offset from the left
            //side of the screen.  Subtract this from the total screen width to find the position relative 
            //to the right side of the screen
            var right_edge = $(window).width() - (left_edge +  $("#report_options").width());

            //Display the panel
            $('.arches-report-options').show();

            //close the panel
            $('.theme-close').click(function () {
                $('.arches-report-options').hide();
            });
        }

        function createVectorLayer(){
            var format = new ol.format.WKT();
            var feature = format.readFeature($('#map-content').val());
            feature.getGeometry().transform('EPSG:4326', 'EPSG:3857');
            var vector = new ol.layer.Vector({
                  source: new ol.source.Vector({
                    features: [feature],
                    visible: true
                  })
                });
            return vector
            }

        function loadLayers(vector){
            var basemaps = [
                      'Road','Aerial'
                    ];
            var layers = [];
            var i, ii;
            for (i = 0, ii = basemaps.length; i < ii; ++i) {
              layers.push(new ol.layer.Tile({
                visible: false,
                preload: Infinity,
                source: new ol.source.BingMaps({
                  key: 'Ak-dzM4wZjSqTlzveKz5u0d4IQ4bRzVI309GxmkgSVr1ewS6iPSrOvOKhA-CJlm3',
                  imagerySet: basemaps[i]
                })
              }));
            }

            layers.push(vector);
            return layers;
        }

        function zoomToLayer(vectorLayer, map){
            var extent = (vectorLayer.getSource().getExtent());
            var size = (map.getSize());
            view.fitExtent(
                extent,
                size
              );
            }

        function switchLayer(){
            var checkedLayer = $('#layerswitcher input[name=layer]:checked').val();
            for (i = 0, ii = layers.length - 1; i < ii; ++i) layers[i].setVisible(i==checkedLayer);
         }

        var vectorLayer = createVectorLayer()
        var layers = loadLayers(vectorLayer);

        var view = new ol.View({
            center: [-13168799.0, 4012635.2],
            zoom: 10
            })

        var map = new ol.Map({
          layers: layers,
          target: 'map',
          view: view
        });

        zoomToLayer(vectorLayer, map)
        $(function() { switchLayer() } );
        $("#layerswitcher input[name=layer]").change(function() { switchLayer() } );

    });

});
