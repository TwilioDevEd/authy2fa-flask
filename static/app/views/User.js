(function() {
    app.views.UserView = app.views.BaseView.extend({
        // name of the template file to load from the server
        templateName: 'user',

        initialize: function() {
            var self = this;
            
            app.router.on('route:user', function() {
                // If we already have token and a user, assume logged in
                if (app.get('token') && app.get('user')) {
                    self.render();
                } else if (!app.get('token')) {
                    self.requireLogin();
                } else {
                    // Make a GET request to a resource secured by our auth
                    // token
                    $.ajax({
                        url:'/user',
                        method:'GET',
                        headers: {
                            'X-API-TOKEN': app.get('token')
                        }
                    }).done(function(data) {
                        app.set('user', data);
                        self.render();
                    }).fail(function(err) {
                        self.requireLogin();
                    });
                }
            });
        },

        // helper for updating app model and navigating to login screen
        requireLogin: function() {
            app.set('message', {
                error: true,
                message: 'You must be logged in to view this page.'
            });
            app.router.navigate('login', {
                trigger: true
            });
        }
    });
})();