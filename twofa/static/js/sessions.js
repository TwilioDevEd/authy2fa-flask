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

      $('#authy-modal').modal({backdrop:'static'},'show');
      if (data.success) {
        $('.auth-ot').fadeIn();
        checkForOneTouch();
      } else {
        redirectToTokenForm();
      }
    });
  };

  var checkForOneTouch = function() {
    $.get( "/login/status", function(data) {
      console.log(data);
      
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
