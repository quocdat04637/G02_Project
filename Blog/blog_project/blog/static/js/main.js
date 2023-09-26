$(document).ready(function () {
    var registrationSuccessful = $('#successModal').data('registration-successful');
    if (registrationSuccessful === 'true') {
      $('#successModal').modal('show');
    }
  });
  