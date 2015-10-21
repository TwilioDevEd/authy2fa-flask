$(document).ready(function() {

  $('#login-form').submit(function(e) {
    e.preventDefault();
    formData = $(e.currentTarget).serialize();
    attemptOneTouchVerification(formData);
  });

  var attemptOneTouchVerification = function(form) {
    $.post( "/sessions", form, function(data) {
      $('#authy-modal').modal({backdrop:'static'},'show');
      if (data.success) {
        $('.auth-ot').fadeIn();
        checkForOneTouch();
      } else {
        $('.auth-token').fadeIn();
      }
    });
  };

  var checkForOneTouch = function() {
    $.get( "/authy/status", function(data) {
      
      if (data == 'approved') {
        window.location.href = "/account";
      } else if (data == 'denied') {
        showTokenForm();
        triggerSMSToken();
      } else {
        setTimeout(checkForOneTouch, 2000);
      }
    });
  };

  var showTokenForm = function() {
    $('.auth-ot').fadeOut(function() {
      $('.auth-token').fadeIn('slow');
    });
  };

  var triggerSMSToken = function() {
    $.get("/authy/send_token");
  };
});
