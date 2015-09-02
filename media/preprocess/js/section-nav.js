var sectionNavigation = (function() {

  var $mainNode = $('main');
  var $columns = $('.column');
  var $columnWrapper = $('.columns-wrapper');

  $('.column').on('click', toggleSection);

  function toggleSection() {
    
    //cache DOM
    var $selection = $(this);
    var $selectionSiblings = $selection.siblings();
    var sectionStr = $selection.data('section');
    var $section = $('.'+ sectionStr);
    var $sectionSiblings = $section.siblings();

    //expand selection horizontally
    $selection.toggleClass('open');
    $selectionSiblings.removeClass('open');

    // shrink horizontally if at least one column is open
    if ($columns.hasClass('open')) {
      $columns.addClass('tabbed');
      $columnWrapper.addClass('shrunk');
    } else {
      $columns.removeClass('tabbed').css({
        'border-bottom':'none'
      });
      $columnWrapper.removeClass('shrunk');
    }

    // expand corresponding section
    if(!$section.hasClass('open')) {
      $section.removeClass('closed').addClass('open');
      $sectionSiblings.removeClass('open').addClass('closed');
    } else {
      $section.removeClass('open').addClass('closed');
    }

    // change background according to the color closed
    if (sectionStr == 'how' || sectionStr == 'work') {
      $mainNode.removeClass('white').addClass('black');
    }
    if (sectionStr == 'we' || sectionStr == 'now') {
      $mainNode.removeClass('black').addClass('white');
    }

    // add bottom border dynamically on click
    if (sectionStr == 'how' && $columns.hasClass('tabbed')) {
      $($columns[2]).css({
        'border-bottom':'4px solid #F9F9F9'
      });
      $($columns[2]).siblings().css({
        'border-bottom':'none'
      });
    }
    if (sectionStr == 'we' && $columns.hasClass('tabbed')) {
      $($columns[3]).css({
        'border-bottom':'4px solid #212121'
      });
      $($columns[3]).siblings().css({
        'border-bottom':'none'
      });
    }
    if (sectionStr == 'work' && $columns.hasClass('tabbed')) {
      $($columns[0]).css({
        'border-bottom':'4px solid #F9F9F9'
      });
      $($columns[0]).siblings().css({
        'border-bottom':'none'
      });
    }
    if (sectionStr == 'now' && $columns.hasClass('tabbed')) {
      $($columns[1]).css({
        'border-bottom':'4px solid #212121'
      });
      $($columns[1]).siblings().css({
        'border-bottom':'none'
      });
    }
  }
})();
