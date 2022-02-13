document.addEventListener('DOMContentLoaded', function() {
  // modal initialization
  var modal = document.querySelectorAll('.modal');
  M.Modal.init(modal);

  // hide messages after 5 seconds
  setTimeout(() => {
    var messages = document.getElementsByClassName('messages');
    messages[0].style.display = 'none';
  }, 5000);
});
