(function() {
    app.views.HomeView = app.views.BaseView.extend({
        // name of the template file to load from the server
        templateName: 'home',

        initialize: function() {
            var self = this;

            // default behavior, render page into #page section
            app.router.on('route:home', function() {
                self.render();
            });
        }
    });
})();