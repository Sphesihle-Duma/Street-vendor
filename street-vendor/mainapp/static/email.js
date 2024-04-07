jQuery.noConflict(); 
jQuery(document).ready(function () {
    jQuery(".notif-button").click(function () {
      var email = jQuery(this).data('email');

      // Confirm the action with the user
      var confirmMessage = "Are you sure you want to send email to" + email.toLowerCase();
      if (!confirm(confirmMessage)) {
        return; // Do nothing if the user cancels the action
      }

      // Send a PUT request to update the permit status
      jQuery.ajax({
        url: "http://127.0.0.1:5000/send_email",
        type: "PUT",
        contentType: "application/json",
        data: JSON.stringify({email: email}),
        success: function (response) {
          console.log(response);
          
          // Update the UI without reloading the page
          //jQuery(`.approve-button[data-email='${email}'], .decline-button[data-email='${email}']`).parent().fadeOut();
          // Optionally display a success message
          //jQuery("#email-status").show().delay(3000).fadeOut(); // Display for 3 seconds and then fade out
        },
        error: function (error) {
          console.error(error);
        },

	complete: function () {
                // Reload the page after the AJAX request is complete
                location.reload();
            }
      });
    });
  });
       
