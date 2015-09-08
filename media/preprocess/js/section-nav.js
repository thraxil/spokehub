
var section = (function() {

  var $mainNode = $('main');
  var $columns = $('.column');
  var $columnWrapper = $('.columns-wrapper');

  $('.column').on('click', toggleSection);

  function toggleSection() {

    //cache DOM
    var $targetColumn = $(this);
    var $columnSiblings = $targetColumn.siblings();
    var sectionString = $targetColumn.data('section');
    var $targetSection = $('.'+ sectionString);
    var $sectionSiblings = $targetSection.siblings();

    //expand selection horizontally
    $targetColumn.toggleClass('open');
    $columnSiblings.removeClass('open');

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
    if($targetSection.hasClass('open')) {
      $targetSection.removeClass('open').addClass('closed');
    } else {
      setTimeout(function() {
        $targetSection.removeClass('closed').addClass('open');
        switch(sectionString) {
          case 'how':

            window.location.pathname = 'how';
            break;
          case 'we':
            window.location.pathname = 'we';
            conversations.resizeText();
            break;
          case 'work':
            window.location.pathname = 'work';
            break;
          case 'now':
            window.location.pathname = 'now';
            break;
        }
      },1000);
      $sectionSiblings.removeClass('open').addClass('closed');
    }

    addBottomBorder(sectionString, $columns);

    // change background according to the color closed
    if (sectionString == 'how' || sectionString == 'work') {
      $mainNode.removeClass('white').addClass('black');
    }
    if (sectionString == 'we' || sectionString == 'now') {
      $mainNode.removeClass('black').addClass('white');
    }
  }

  function checkWindowLocation() {
    var windowLocation = window.location.pathname;
    var $columns = $('.column');

    switch (windowLocation) {
      case '/how':

        var target = $columns.data('section', 'how');
        var siblings = target.siblings();

        target.addClass('open tabbed');
        siblings.addClass('tabbed');
        addBottomBorder('how', $columns);

        $('section.how').removeClass('closed').addClass('open');


        break;
      case '/we':

        var target = $columns.data('section', 'we');
        var siblings = target.siblings();

        target.addClass('open tabbed');
        siblings.addClass('tabbed');
        addBottomBorder('how', $columns);

        setTimeout(function(){
          $('section.we').removeClass('closed').addClass('open');
          conversations.resizeText();
        });

        break;
      case '/work':

        var target = $columns.data('section', 'work');
        var siblings = target.siblings();

        target.addClass('open tabbed');
        siblings.addClass('tabbed');
        addBottomBorder('how', $columns);

        $('section.work').removeClass('closed').addClass('open');

        break;
      case '/now':

        var target = $columns.data('section', 'now');
        var siblings = target.siblings();

        target.addClass('open tabbed');
        siblings.addClass('tabbed');
        addBottomBorder('how', $columns);

        $('section.now').removeClass('closed').addClass('open');

        break;
      default:
        return;
    }
  }

  function addBottomBorder(target, columns) {
    // add bottom border dynamically on click
    if (target == 'how' && columns.hasClass('tabbed')) {
      $(columns[2]).css({
        'border-bottom':'4px solid #F9F9F9'
      });
      $(columns[2]).siblings().css({
        'border-bottom':'none'
      });
    }
    if (target == 'we' && columns.hasClass('tabbed')) {
      $(columns[3]).css({
        'border-bottom':'4px solid #212121'
      });
      $(columns[3]).siblings().css({
        'border-bottom':'none'
      });
    }
    if (target == 'work' && columns.hasClass('tabbed')) {
      $(columns[0]).css({
        'border-bottom':'4px solid #F9F9F9'
      });
      $(columns[0]).siblings().css({
        'border-bottom':'none'
      });
    }
    if (target == 'now' && columns.hasClass('tabbed')) {
      $(columns[1]).css({
        'border-bottom':'4px solid #212121'
      });
      $(columns[1]).siblings().css({
        'border-bottom':'none'
      });
    }
  }

  checkWindowLocation();

  return {
    checkWindowLocation: checkWindowLocation
  }

})()
