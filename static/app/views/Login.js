(function() {
    app.views.LoginView = app.views.BaseView.extend({
        // name of the template file to load from the server
        templateName: 'login',

        // UI events
        events: {
            'submit #loginForm': 'login'
        },

        initialize: function() {
            var self = this;
            // default behavior, render page into #page section
            app.router.on('route:login', function() {
                self.render();
            });
        },

        // Hit login service
        login: function(e) {
            var self = this;

            e.preventDefault();
            app.set('message', null);

            $.ajax('/session', {
                method: 'POST',
                data: {
                    email: self.$('#email').val(),
                    password: self.$('#password').val()
                }
            }).done(function(data) {
                // If it succeeded, store API token and go to validation
                // step
                app.set('token', data.token);
                app.router.navigate('verify', {
                    trigger: true
                });
            }).fail(function(err) {
                app.set('message', {
                    error: true,
                    message: err.responseJSON.message ||
                        'Sorry, an error occurred, please log in again.'
                });
            });
        }
    });
})();