/* Filename: base.js */
//$(document).ready(function() {
//	$('ul.nav a').hover(function() {
//		$('#triangle-up').css('border-bottom','30px solid #bcd2ee');
//	}, function() {
//	//on mouseout, reset the color
//	$('#triangle-up').css('border-bottom','30px solid #3D3D3D');
//	});
//});

  $(document).ready(function () { 
    var newHeight = $(window).height() - $('#header-wrapper').height() - $('#menu-wrapper').height() - $('#copyright').height();
    var oldHeight = $('#featured-wrapper').height();

    if (newHeight > oldHeight) {
      $('#featured-wrapper').height(newHeight);
    }
  });


//Makes the nav bar sticky whenever it reaches the top
$(document).ready(function () {

	var menu = $('#menu-wrapper');
	var origOffsetY = menu.offset().top;

	function scroll() {
		if ($(window).scrollTop() >= origOffsetY) {
			$('#menu-wrapper').addClass('navbar-fixed-top');
			$('.wrapper').addClass('menu-padding');
		} else {
			$('#menu-wrapper').removeClass('navbar-fixed-top');
			$('.wrapper').removeClass('menu-padding');
		}

	}

	document.onscroll = scroll;

});
