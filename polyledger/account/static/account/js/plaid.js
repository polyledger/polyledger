(function($) {
  function getCookie(c_name) {
    if (document.cookie.length > 0) {
      c_start = document.cookie.indexOf(c_name + "=");
      if (c_start != -1) {
        c_start = c_start + c_name.length + 1;
        c_end = document.cookie.indexOf(";", c_start);
        if (c_end == -1) c_end = document.cookie.length;
        return unescape(document.cookie.substring(c_start,c_end));
      }
    }
    return "";
  }

  $.ajaxSetup({
    headers: { "X-CSRFToken": getCookie("csrftoken") }
  });

  var handler = Plaid.create({
    apiVersion: 'v2',
    clientName: 'Polyledger',
    env: 'sandbox',
    product: ['auth'],
    key: 'af5c2e7385fc3f941340c29c8c88db',
    onSuccess: function(public_token) {
      $.post('/account/get_access_token/', { public_token: public_token }, function(response) {
        console.log(response);
      });
    },
  });

  $('#link-btn').on('click', function(e) {
    handler.open();
  });

})(jQuery);