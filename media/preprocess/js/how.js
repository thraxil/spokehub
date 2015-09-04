var how = (function() {

  var $images = $('.how-image');

  $images.on('click', function() {
    var nextImage = $(this).next();
    if($(this).index() < $images.length - 1) {
      nextImage.fadeToggle('300');
      $(this).fadeToggle('300');
    } else {
      $(this).fadeToggle('300');
      $($images[0]).fadeToggle('300');
    }
  });

  return {
    slideshow: {
      images: $images
    }
  }
})()
