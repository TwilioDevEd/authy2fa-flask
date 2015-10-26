$(document).ready(function() {

  $('#login-form').submit(function(e) {
    e.preventDefault();
    formData = $(e.currentTarget).serialize();
    attemptOneTouchVerification(formData);
  });

  var attemptOneTouchVerification = function(form) {
    $.post( "/login", form, function(data) {
      // Check first if we successfully authenticated the username and password
      if (data.hasOwnProperty('invalid_credentials')) {
        $('.form-errors').remove();
        $('#login-form').prepend(data.invalid_credentials);
        return;
      }

      if (data.success) {
        $('#authy-modal').modal({backdrop:'static'},'show');
        $('.auth-ot').fadeIn();
        checkForOneTouch();
      } else {
        redirectToTokenForm();
      }
    });
  };

  var checkForOneTouch = function() {
    $.get( "/login/status", function(data) {
      
      if (data == 'approved') {
        window.location.href = "/account";
      } else if (data == 'denied') {
        redirectToTokenForm();
      } else {
        setTimeout(checkForOneTouch, 2000);
      }
    });
  };

  var redirectToTokenForm = function() {
    window.location.href = "/verify";
  };
});
