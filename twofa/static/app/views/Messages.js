(function() {
    app.views.MessagesView = app.views.BaseView.extend({
        // name of the template file to load from the server
        templateName: 'messages',

        // Mount to messages section
        el: '#messages',

        // UI events
        events: {
            'click i': 'close'
        },

        initialize: function() {
            var self = this;
            // Render whenever there is a message on the global app model
            app.on('change:message', function() {
                self.render();
            });
        },

        // close messages section by removing content 
        // from the containing elem
        close: function(e) {
            e && e.preventDefault();
            this.$el.html('');
        },

        // render messages content
        render: function() {
            var self = this;
            
            // Fetch template from server and render when ready, since it
            // is the initial template for the app
            if (!self.template) {
                // self.templateName should be configured to be the name of
                // the Lodash HTML template file in the "app/templates"
                // directory
                self.getTemplate(self.templateName, function(tpl) {
                    self.template = tpl;
                    self.render();
                });
            } else {
                // Template is loaded, so render
                var m = app.get('message');
                if (m) {
                    // if we have a message, render the template
                    self.$el.html(self.template(m));
                } else {
                    // otherwise, close out the UI element
                    self.close();
                }
            }
        }
    });
})();