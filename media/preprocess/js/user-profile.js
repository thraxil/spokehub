var user = (function() {

  var $userCard = $('div.card-profile');

  function saveProfile() {
    var username = $('.name-input input').val();
    var title = $('.title-input input').val();
    var location = $('.location-input input').val();
    var websiteUrl = $('.website-input input').val();

    console.log(
      username,
      title,
      location,
      websiteUrl
    );
  }

  $('#user-link').click(function (e) {
      $($userCard).fadeToggle('fast');
      e.stopImmediatePropagation();
  });

  $(document).click(function (e) {
      if($userCard.css('display') == 'block' && !$userCard.is(e.target)) {
        $($userCard).fadeToggle('fast');
      }
  });

  return {
    saveProfile: saveProfile
  };

})()
