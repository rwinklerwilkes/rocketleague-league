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


google.load('visualization','1.0',{'packages':['corechart']});

$(document).ready(function () {
	chartData('All','All','1,0,0,0,0');
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
	
	var possible_cols = ['Week','Goals','Assists','Saves','Shots','Points']

	var col1 = stats[0][0];
	var numSeries = stats[0].length-1;
	//Column 0 will always have 'Week', so we can skip this in the loop
	data.addColumn('string',col1);
	var seriesPrep = {};
	var axesPrep = {0:{title:'Number'},1:{title:'Points'}};
	
	for(i=1;i<stats[0].length;i++)
	{
		console.log(stats[0][i]);
		data.addColumn('number',stats[0][i]);
		if (stats[0][i]==='points') {
			var j = i -1;
			seriesPrep[j] = {targetAxisIndex:1};
		}
		else {
			var j = i -1;
			seriesPrep[j] = {targetAxisIndex:0};
		}
	}
	console.log(seriesPrep);
	console.log(axesPrep);

	for (i=1;i<stats.length;i++) {
		data.addRow(stats[i]);
	}

	var materialOptions = {
		title: 'Performance by Season and Week',
		chartArea: {left:0, top:20},
		curveType: 'function',
		width: $(document).width()/3,
		height: 400
	};
	materialOptions.series = seriesPrep;
	materialOptions.vAxes = axesPrep;
	
	var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

	chart.draw(data,materialOptions);
}


$(function() {
	$(".dropdown-menu").on('click','li a', function () {
		var btn = $('.btn#' + $(this).parents('ul').attr('id'));
		btn.html($(this).text() + ' <span class="caret"></span>');
		btn.val($(this).text());
		
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
			chartData(otBtn.val(),btn.val(),allValues());
		}
		else {
			chartData(btn.val(),otBtn.val(),allValues());
		}
	});
});

function allValues() {
	var allVals = [];
	$("#chart_Btns input").each(function () {
		if ($(this).prop('checked')) {
			allVals.push(1);
		} else {
			allVals.push(0);
		}
	});
	var outstr = "";
	for(i=0;i<allVals.length;i++) {
		outstr += parseInt(allVals[i],10);
		outstr += ",";
	}
	outstr = outstr.slice(0,-1);
	
	return outstr;
}

$(function () {
	$("#chart_Btns input").click(function() {
		var otstr = allValues();
		var seasonbtn = $('.btn#season-dropdown').val();
		var weekbtn = $('.btn#week-dropdown').val();
		chartData(seasonbtn,weekbtn,otstr);
	});
});

