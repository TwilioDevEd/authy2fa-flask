(function() {
    app.views.NavView = app.views.BaseView.extend({
        // name of the template file to load from the server
        templateName: 'nav',

        // Mount to messages section
        el: '#nav-links',

        // UI Events
        events: {
            'click #logout': 'logout'
        },

        initialize: function() {
            var self = this;
            app.on('change:user', function() {
                self.render();
            });

            // initially render immediately
            self.render();
        },

        // Log a user out of the application
        logout: function(e) {
            var self = this;
            e.preventDefault();
            app.set('message', null);

            // Destroy the current session
            $.ajax('/session', {
                method: 'DELETE',
                headers: {
                    'X-API-TOKEN': app.get('token')
                }
            }).done(function() {
                app.logoutUser();
            }).fail(function(err) {
                app.set('message', {
                    error: true,
                    message: err.responseJSON.message ||
                        'Sorry, an error occurred, please log out again.'
                });
            });
        }
    });
})();