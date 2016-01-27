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
google.setOnLoadCallback(drawChart);

$(document).ready(function () {
	$.ajax(
	{
	type:'GET',
	url:'/schedule/chart_data/',
	data:{'season':201601,'week':'All','out':'goals'},
	success:function(dataFromServer) {drawChart(dataFromServer);}
	}
	);
});

//creates and populates data table, instantiates chart, passes in data, and draws
function drawChart(dataFromServer) {
	var data = new google.visualization.DataTable();
	
	var stats = dataFromServer['stats'];

	var col1 = stats[0][0];
	var col2 = stats[0][1];
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

