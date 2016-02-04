$(document).ready(function() {
	$('#calendar').fullCalendar({
		header: {
			left:'prev,next',
			center:'title',
			right:'month,agendaWeek'
		},
		defaultView: 'agendaWeek',
		googleCalendarApiKey: 'AIzaSyCcwjHklrf3eTaMZyzmJrrgPj3jVWY5bH0',
		events: {
			googleCalendarId: 'd8mt6rrgs00gglo8l0di9p2atk@group.calendar.google.com'
		}
	});
});