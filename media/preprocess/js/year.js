var date = (function() {
  var year = new Date().getFullYear();
  var $footer = $('footer');

  $footer.on('load', placeDate());

  function placeDate() {
    $('.year').html(year);
  }
})()
