// Bootstap the front-end application
$(document).ready(function() {
    // Create UI views
    var home = new app.views.HomeView();
    var login = new app.views.LoginView();
    var signup = new app.views.SignupView();
    var verify = new app.views.VerifyView();
    var nav = new app.views.NavView();
    var user = new app.views.UserView();
    var messages = new app.views.MessagesView();

    // Start URL router
    Backbone.history.start();
});