var how=function(){var $images=$(".how-image");return $images.on("click",function(){var nextImage=$(this).next();$(this).index()<$images.length-1?(nextImage.fadeToggle("300"),$(this).fadeToggle("300")):($(this).fadeToggle("300"),$($images[0]).fadeToggle("300"))}),{slideshow:{images:$images}}}(),instagram=function(){var $videos=$(".now-post.instagram video");console.log($videos[0]),$videos.each(function(index,value){$(value).after('<i class="mdi mdi-play-circle"></i>'),$(value).on("click",function(){1==value.paused?(value.play(),$(value).siblings().fadeToggle("fast")):(value.pause(),$(value).siblings().fadeToggle("fast"))})})}(),section=function(){function toggleSection(){var $targetColumn=$(this),$columnSiblings=$targetColumn.siblings(),sectionString=$targetColumn.data("section"),$targetSection=$("."+sectionString),$sectionSiblings=$targetSection.siblings();$targetColumn.toggleClass("open"),$columnSiblings.removeClass("open"),$columns.hasClass("open")?($columns.addClass("tabbed"),$columnWrapper.addClass("shrunk")):($columns.removeClass("tabbed").css({"border-bottom":"none"}),$columnWrapper.removeClass("shrunk")),$targetSection.hasClass("open")?$targetSection.removeClass("open").addClass("closed"):(setTimeout(function(){switch($targetSection.removeClass("closed").addClass("open"),sectionString){case"how":break;case"we":conversations.resizeText();break;case"work":break;case"now":}},1e3),$sectionSiblings.removeClass("open").addClass("closed")),addBottomBorder(sectionString,$columns),("how"==sectionString||"work"==sectionString)&&$mainNode.removeClass("white").addClass("black"),("we"==sectionString||"now"==sectionString)&&$mainNode.removeClass("black").addClass("white")}function checkWindowLocation(){var windowLocation=window.location.pathname,$columns=$(".column");switch(windowLocation){case"/how":var target="how"==$columns.data("section"),siblings=target.siblings();target.addClass("open tabbed"),siblings.addClass("tabbed"),addBottomBorder("how",$columns),$("section.how").removeClass("closed").addClass("open");break;case"/we":var target="we"==$columns.data("section"),siblings=target.siblings();target.addClass("open tabbed"),siblings.addClass("tabbed"),addBottomBorder("how",$columns),$("section.we").removeClass("closed").addClass("open");break;case"/work":var target="work"==$columns.data("section"),siblings=target.siblings();target.addClass("open tabbed"),siblings.addClass("tabbed"),addBottomBorder("how",$columns),$("section.work").removeClass("closed").addClass("open");break;case"/now":var target="now"==$columns.data("section"),siblings=target.siblings();target.addClass("open tabbed"),siblings.addClass("tabbed"),addBottomBorder("how",$columns),$("section.now").removeClass("closed").addClass("open");break;default:return}}function addBottomBorder(target,columns){"how"==target&&columns.hasClass("tabbed")&&($(columns[2]).css({"border-bottom":"4px solid #F9F9F9"}),$(columns[2]).siblings().css({"border-bottom":"none"})),"we"==target&&columns.hasClass("tabbed")&&($(columns[3]).css({"border-bottom":"4px solid #212121"}),$(columns[3]).siblings().css({"border-bottom":"none"})),"work"==target&&columns.hasClass("tabbed")&&($(columns[0]).css({"border-bottom":"4px solid #F9F9F9"}),$(columns[0]).siblings().css({"border-bottom":"none"})),"now"==target&&columns.hasClass("tabbed")&&($(columns[1]).css({"border-bottom":"4px solid #212121"}),$(columns[1]).siblings().css({"border-bottom":"none"}))}var $mainNode=$("main"),$columns=$(".column"),$columnWrapper=$(".columns-wrapper");return $(".column").on("click",toggleSection),checkWindowLocation(),{checkWindowLocation:checkWindowLocation}}(),user=function(){function saveProfile(){var username=$(".name-input input").val(),title=$(".title-input input").val(),location=$(".location-input input").val(),websiteUrl=$(".website-input input").val();console.log(username,title,location,websiteUrl)}var $userCard=$("div.card-profile");return $("#user-link").click(function(e){$($userCard).fadeToggle("fast"),e.stopImmediatePropagation()}),$(document).click(function(e){"block"!=$userCard.css("display")||$userCard.is(e.target)||$($userCard).fadeToggle("fast")}),{saveProfile:saveProfile}}(),conversations=function(){function resizeText(){for(var i=0;i<$cards.length;i++)$($cards[i]).find(".conversation-title").textTailor({maxFont:72})}var $cards=$(".card-conversation");return{resizeText:resizeText}}(),date=function(){function placeDate(){$(".year").html(year)}var year=(new Date).getFullYear(),$footer=$("footer");$footer.on("load",placeDate())}();