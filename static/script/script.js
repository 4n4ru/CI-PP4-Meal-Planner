document.addEventListener('DOMContentLoaded', function() {
  // modal initialization
  var modal = document.querySelectorAll('.modal');
  M.Modal.init(modal);

  // sidenav initialization
  var sidenav = document.querySelectorAll('.sidenav');
  M.Sidenav.init(sidenav);

  // tooltip initialization
  var tooltip = document.querySelectorAll('.tooltipped');
  M.Tooltip.init(tooltip);

  // hide messages after 5 seconds
  setTimeout(() => {
    var messages = document.getElementsByClassName('messages')[0]
    if (messages) {
      messages.style.display = 'none';
    }
  }, 5000);
});
