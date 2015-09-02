var conversations = (function() {

  var $cards = $('.card-conversation');

  function resizeText() {
    for(var i = 0; i < $cards.length; i++) {
      $($cards[i]).find('.conversation-title').textTailor({
        maxFont: 72
      });
    }
  }

  return {
    resizeText: resizeText
  }
})();
