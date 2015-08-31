var sectionNavigation = (function() {
  var $columns = $('.column');
  var $columnWrapper = $('.columns-wrapper');
  $('.column').on('click', toggleSection);

  function toggleSection() {
    //cache DOM
    var $selection = $(this);
    var section = $selection.data('section');
    var $siblings = $selection.siblings();

    //expand selection horizontally
    $selection.toggleClass('open');
    $siblings.removeClass('open');

    // shrink horizontally if at least one column is open
    if ($columns.hasClass('open')) {
      $columns.addClass('tabbed');
      $columnWrapper.addClass('shrunk');
    } else {
      $columns.removeClass('tabbed');
      $columnWrapper.removeClass('shrunk');
    }

    // expand corresponding section
    if ($selection.hasClass('open')) {
      $('.' + section).addClass('open');
    } else {
      $('.' + section).removeClass('open');
    }
  }
})();


// $(function(){
//   'use strict';
//   $('.column').click(function(){
//
//     var target = $(this);
//     var others = $(this).siblings();
//     var sectionTarget = target.attr('id');
//
//     target.addClass('expanded');
//
//     others.removeClass('expanded');
//
//     $('.column').each(function(){
//       if ($(this).hasClass('full-column')){
//         $(this).removeClass('full-column');
//         $(this).addClass('tabed-column');
//       }
//     });
//
//     $('.main-section').each(function(){
//       if ($(this).data('target') === sectionTarget) {
//         $(this).addClass('show');
//         $(this).removeClass('hide');
//       } else {
//         $(this).removeClass('show').addClass('hide');
//
//       }
//     });
//   });
//   $('#header-wrapper h2').click(function(){
//     $('.main-section').each(function(){
//       $(this).addClass('hide');
//       $(this).removeClass('show');
//     });
//     $('.column').addClass('full-column').removeClass('tabed-column').removeClass('expanded');
//   });
// });
//
// // Slide getter
//
// var Slider = function(sliderDom) {
//   this.slider = sliderDom;
//   this.currentIndex = 0;
//
//   var self = this;
//
//   $('<button>')
//   .addClass('prev')
//   .on('click', function(){
//     self.displayImage(self.currentIndex - 1);
//   })
//   .appendTo(this.slider);
//
//   $('<button>')
//   .addClass('next')
//   .on('click', function(){
//     self.displayImage(self.currentIndex + 1);
//   })
//   .appendTo(this.slider);
//
//   //Show first picture
//
//   this.displayImage(this.currentIndex);
//
//   setInterval(function() {
//     if ($('#how-column').hasClass('expanded')){
//       if (self.currentIndex === self.slider.children('img').length - 1){
//         self.displayImage(0);
//       } else {
//         self.displayImage(self.currentIndex + 1);
//       }
//     }
//   }, 7000);
//
// };
//
// $(function(){
//   $('.slider').each(function(){
//     new Slider($(this));
//   });
// });
//
// // Slideshow Object
//
// Slider.prototype.displayImage = function(imageIndex) {
//   var numberOfImages = this.slider.children('img').length;
//   if (imageIndex < 0 || imageIndex > numberOfImages){
//     return;
//   }
//
//   this.slider.children('img.visible').removeClass('visible');
//   this.slider.children('img:nth-of-type(' + (imageIndex + 1) + ')').addClass('visible');
//
//   var prevButton = this.slider.children('.prev');
//   if (imageIndex === 0) {
//     prevButton.hide();
//   } else {
//     prevButton.show();
//   }
//
//   var nextButton = this.slider.children('.next');
//
//   if (imageIndex === numberOfImages - 1) {
//     nextButton.hide();
//   } else {
//     nextButton.show();
//   }
//
//   this.currentIndex = imageIndex;
// };
//
// var Fader = function(faderDom) {
//   this.fader = faderDom;
//   this.currentIndex = 0;
//
//   var self = this;
//
//   self.displayImage(self.currentIndex);
//
//   setInterval(function() {
//     if (self.currentIndex === self.fader.children('img').length - 1){
//       self.displayImage(0);
//     } else {
//       self.displayImage(self.currentIndex + 1);
//     }
//   }, 10000);
//
// };
//
// $(function(){
//   $('.fader').each(function(){
//     new Fader($(this));
//   });
// });
//
// Fader.prototype.displayImage = function(imageIndex) {
//   var numberOfImages = this.fader.children('img').length;
//   if (imageIndex < 0 || imageIndex > numberOfImages){
//     return;
//   }
//
//   this.fader.children('img.spotlight').removeClass('spotlight');
//   this.fader.children('img:nth-of-type(' + (imageIndex + 1) + ')').addClass('spotlight');
//
//   this.currentIndex = imageIndex;
// };
