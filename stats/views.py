from django.shortcuts import render, get_object_or_404
from .models import Player, Team, Season, GameWeek
from .models import Game, GameStats

# Create your views here.
def index(request):
    players = Player.objects.all()
    return render(request,'stats/index.html',{'players':players})

def season(request,season_slug):
    season = get_object_or_404(Season,slug=season_slug)
    weeks = season.gameweek_set.all()
    return render(request,'stats/season.html',{'season':season,'weeks':weeks})

def week(request,season_slug,week_number):
    season = get_object_or_404(Season,slug=season_slug)
    week = get_object_or_404(GameWeek,season=season,number=week_number)
    games = week.game_set.all().order_by('series_number')
    return render(request,'stats/week.html',{'season':season,'week':week,'games':games})
