var user = (function() {

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

  return {
    saveProfile: saveProfile
  };

})();
