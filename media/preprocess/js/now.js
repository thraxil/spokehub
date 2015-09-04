var instagram = (function() {
  var $videos = $('.now-post.instagram video');
  console.log($videos[0]);

  $videos.each(function(index, value) {
    $(value).after('<i class="mdi mdi-play-circle"></i>');
    $(value).on('click', function() {
      if (value.paused == true) {
        value.play();
        $(value).siblings().fadeToggle('fast');
      } else {
        value.pause();
        $(value).siblings().fadeToggle('fast');
      }
    });
  });
})()
