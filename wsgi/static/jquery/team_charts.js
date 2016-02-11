/* Filename: base.js */
//$(document).ready(function() {
//	$('ul.nav a').hover(function() {
//		$('#triangle-up').css('border-bottom','30px solid #bcd2ee');
//	}, function() {
//	//on mouseout, reset the color
//	$('#triangle-up').css('border-bottom','30px solid #3D3D3D');
//	});
//});
var curseason="201601";

google.load('visualization','1.0',{'packages':['corechart']});

function chartData(season,team,out,divToUse) {
	$.ajax(
		{
		type:'GET',
		url:'/stats/team_data/',
		data:{'season':season,'team':team,'out':out},
		success:function(dataFromServer) {drawChart(dataFromServer,divToUse);}
		}
	);
}

//creates and populates data table, instantiates chart, passes in data, and draws
function drawChart(dataFromServer,divToUse) {
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
	
	var chart = new google.visualization.LineChart(document.getElementById(divToUse));

	chart.draw(data,materialOptions);
}

//curseason set at top of string
//I should probably fix that to not be hardcoded... not sure how
$(function() {
	$("#accordion").on('click','a', function() {
		var id = $(this).attr("id").slice(-1);
		var defstr = "1,1,1,1,1";
		var divstr = "chart" + id;
		chartData(curseason,id,defstr,divstr);
	});
});

