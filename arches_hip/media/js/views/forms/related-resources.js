define(['jquery', 'views/forms/base'], function ($, BaseForm) {
    return BaseForm.extend({
        
        events: function(){
            var events = BaseForm.prototype.events.apply(this);
            events['click .start-workflow-btn'] = 'startWorkflow';
            return events;
        },


        initialize: function() {
            BaseForm.prototype.initialize.apply(this);
        },

        startWorkflow: function(evt) {
            evt.preventDefault();

            console.log('asfasdf');
        }
    });
});