/* Filename: base.js */

/*
  $(document).ready(function () { 
    var newHeight = $(window).height() - $('#header-wrapper').height() - $('#menu-wrapper').height() - $('#copyright').height();
    var oldHeight = $('#featured-wrapper').height();

    if (newHeight > oldHeight) {
      $('#featured-wrapper').height(newHeight);
    }
  });
*/

//Makes the nav bar sticky whenever it reaches the top

$(document).ready(function () {

	var menu = $('#menu-wrapper');
	var origOffsetY = menu.offset().top;

	function scroll() {
		if ($(window).scrollTop() >= origOffsetY) {
			$('#menu-wrapper').addClass('navbar-fixed-top');
			//$('.wrapper').addClass('menu-padding');
			//75 px is height of menu
			$('.wrapper').css('padding-top','75px');
		} else {
			$('#menu-wrapper').removeClass('navbar-fixed-top');
			//$('.wrapper').removeClass('menu-padding');
			$('.wrapper').css('padding-top','0px');
		}

	}

	document.onscroll = scroll;

});

$(document).ready(function(){
    $('li.dropdown').hover(function() {
		$(this).find('.dropdown-menu').stop(true, true).delay(200).fadeIn(200);
		$(this).css({
			"background": "#bcd2ee",
			"height": "75px"
		});
    }, function() {
		$(this).find('.dropdown-menu').stop(true, true).delay(200).fadeOut(200);
		$(this).css({
			"background": "#3D3D3D"
		});
    });  
});