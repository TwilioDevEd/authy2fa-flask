(function() {
    // Map hash routes to views in the application
    var Router = Backbone.Router.extend({
        routes: {
            '': 'home',
            'home': 'home',
            'signup': 'signup',
            'login': 'login',
            'verify': 'verify',
            'user': 'user'
        }
    });

    app.router = new Router();
})();