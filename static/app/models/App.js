(function() {
    // window-scoped "app" model serves as the global state for our application 
    // and a namespace for any modules within our application
    var AppModel = Backbone.Model.extend({
        // store router at the app level
        router: null,

        // namespace for Backbone View constructors
        views: {},

        // default model attributes
        defaults: {
            user: null,
            token: null,
            message: null
        },

        // Clear any informational message
        clearMessage: function() {
            var self = this;
            self.set('message', null);
        },

        // Log out current user
        logoutUser: function() {
            var self = this;
            self.set({
                'user': null,
                'message': null,
                'token': null
            });
            app.router.navigate('home', {
                trigger: true
            });
        }

    });

    // create an instance of the global app model 
    window.app = new AppModel();
})();