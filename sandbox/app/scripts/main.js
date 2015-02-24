'use strict';

$(document).ready(function(){
  $('.section-link').click(function(){
    var target = $(this).closest('section');
    console.log(target);
    if (target.hasClass('active')) {
      target.removeClass('active');
    } else {
      target.addClass('active');
    }
  });
});
