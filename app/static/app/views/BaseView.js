(function() {
    // Base view controller other views will extend, encapsulate common view
    // functionality
    app.views.BaseView = Backbone.View.extend({

        // Most views in this application will bind to the same page element
        el: '#page',

        // render template into target div
        render: function() {
            var self = this;
            self.renderTemplate(app.attributes);
        },

        // provide a means to load Lodash templates from the server. UI
        // templates are found in app/templates
        getTemplate: function(name, callback) {
            $.get('/app/templates/'+name+'.html').done(function(tpl) {
                // Compile and return a template function
                var compiledTemplate = _.template(tpl);
                callback.call(this, compiledTemplate);
            }).fail(function(err) {
                // Couldn't fetch and compile a template function
                console.error('Failed to load template from server: '+name);
                callback.call(this, function() {
                    return 'error loading template "'+name+'" :(';
                });
            });
        },

        // render this view's template, fetched from the server
        renderTemplate: function(context) {
            var self = this, ctx = context||{};
            
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
                // Render template with attributes from the global app model
                self.$el.html(self.template(ctx));
            }
        }

    });

})();