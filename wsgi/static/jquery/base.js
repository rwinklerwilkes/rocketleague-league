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


google.load('visualization','1.0',{'packages':['corechart']});

$(document).ready(function () {
	chartData('All','All','goals');
});

function chartData(season,week,out) {
	$.ajax(
	{
	type:'GET',
	url:'/schedule/chart_data/',
	data:{'season':season,'week':week,'out':out},
	success:function(dataFromServer) {drawChart(dataFromServer);}
	}
	);
}

//creates and populates data table, instantiates chart, passes in data, and draws
function drawChart(dataFromServer) {
	var data = new google.visualization.DataTable();
	
	var stats = dataFromServer['stats'];
	console.log(stats);

	var col1 = stats[0][0];
	console.log(col1)
	var col2 = stats[0][1];
	console.log(col2)
	data.addColumn('string',col1);
	data.addColumn('number',col2);
	
	for (i=1;i<stats.length;i++) {
		data.addRow(stats[i]);
	}

	var options = {
	width: $(window).width()/3,
	height: 400,
	hAxis: {
		title: 'Game'
	},
	vAxis: {
		title: 'Points Scored'
	}
	};

	var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

	chart.draw(data,options);
}


$(function() {
	$(".dropdown-menu").on('click','li a', function () {
		var btn = $('.btn#' + $(this).parents('ul').attr('id'));
		btn.html($(this).text() + ' <span class="caret"></span>');
		//btn.val($(this).data('value'));
		
		var other = '';
		//call function to redraw graph
		if ($(this).parents('ul').attr('id')=='week-dropdown') {
			other = 'season-dropdown';
		}
		else {
			other = 'week-dropdown';
		}
		var otBtn = $('.btn#' + other);
		
		if (other == 'season-dropdown') {
			chartData(otBtn.text(),$(this).text(),'goals');
		}
		else {
			chartData($(this).text(),otBtn.text(),'goals');
		}
	});
});

