(function() {
    app.views.VerifyView = app.views.BaseView.extend({
        // name of the template file to load from the server
        templateName: 'verify',

        // UI Events
        events: {
            'submit #verifyForm': 'verify',
            'click #verifyForm a': 'resend'
        },

        initialize: function() {
            var self = this;
            // default behavior, render page into #page section
            app.router.on('route:verify', function() {
                self.render();
            });
        },

        // Send the validation code to the server to complete login
        verify: function(e) {
            var self = this;

            e.preventDefault();
            app.set('message', null);

            $.ajax('/session/verify', {
                method: 'POST',
                headers: {
                    'X-API-TOKEN': app.get('token')
                },
                data: {
                    code: self.$('#code').val()
                }
            }).done(function(data) {
                // Now we're logged in! Store the user's information
                app.router.navigate('user', {
                    trigger: true
                });
            }).fail(function(err) {
                app.set('message', {
                    error: true,
                    message: err.responseJSON.message ||
                        'Sorry, an error occurred, please try again.'
                });
            });
        },

        // Resend the validation code via authy
        resend: function(e) {
            var self = this;

            e.preventDefault();
            app.set('message', null);

            $.ajax('/session/resend', {
                method: 'POST',
                headers: {
                    'X-API-TOKEN': app.get('token')
                }
            }).done(function(data) {
                app.set('message', {
                    error: false,
                    message: 'Code re-sent!'
                });
            }).fail(function(err) {
                app.set('message', {
                    error: true,
                    message: err.responseJSON.message ||
                        'Sorry, an error occurred, please try again.'
                });
            });
        }
    });
})();