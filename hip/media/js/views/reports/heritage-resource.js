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
            
            //alert("offset " + offset + " left edge " + left_edge + " right edge " + right_edge);

            //Display the panel
            $('.arches-report-options').show();

            //close the panel
            $('.theme-close').click(function () {
                $('.arches-report-options').hide();
            });
        }

        var styles = [
                  'Aerial','Road','AerialWithLabels','collinsBart','ordnanceSurvey'
                ];

        var layers = [];
        var i, ii;
        for (i = 0, ii = styles.length; i < ii; ++i) {
          layers.push(new ol.layer.Tile({
            visible: false,
            preload: Infinity,
            source: new ol.source.BingMaps({
              key: 'Ak-dzM4wZjSqTlzveKz5u0d4IQ4bRzVI309GxmkgSVr1ewS6iPSrOvOKhA-CJlm3',
              imagerySet: styles[i]
            })
          }));
        }
        var map = new ol.Map({
          layers: layers,
          target: 'map',
          view: new ol.View({
                center: [-13168799.0, 4012635.2],
                zoom: 10
          })
        });

        $('#layer-select').change(function() {
          var style = $(this).find(':selected').val();
          var i, ii;
          for (i = 0, ii = layers.length; i < ii; ++i) {
            layers[i].setVisible(styles[i] == style);
          }
        });
        $('#layer-select').trigger('change');


    });

});
