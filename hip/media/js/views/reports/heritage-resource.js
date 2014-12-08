require([
    'jquery',
    'arches',
    "bootstrap"
], function($, arches) {
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

    });

});
