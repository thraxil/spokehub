'use strict';

$(document).ready(function(){
  $('.column').click(function(){

    var target = $(this);
    var others = $(this).siblings();
    var sectionTarget = target.attr('id');

    target.addClass('expanded');

    others.removeClass('expanded');

    $('.column').each(function(){
      if ($(this).hasClass('full-column')){
        $(this).removeClass('full-column');
        $(this).addClass('tabed-column');
      }
    });

    $('.main-section').each(function(){
      if ($(this).data('target') === sectionTarget) {
        $(this).addClass('show');
      } else {
        $(this).removeClass('show').addClass('hide');

      }
    });
  });
  $('#header-wrapper h2').click(function(){
    $('.main-section').each(function(){
      $(this).addClass('hide');
      $(this).removeClass('show');
    });
    $('.column').addClass('full-column').removeClass('tabed-column').removeClass('expanded');
  });
});
