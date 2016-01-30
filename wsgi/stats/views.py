from django.shortcuts import render, get_object_or_404
from .models import Player, Team, Season, GameWeek
from .models import Game, GameStats

# Create your views here.
def index(request):
    season = Season.objects.all()
    return render(request,'stats/index.html',{'season':season})

def players(request):
    players = Player.objects.all()
    #update stats
    for p in players:
        p.update_stats()
    return render(request,'stats/players.html',{'players':players})

def season(request,season_slug):
    season = get_object_or_404(Season,slug=season_slug)
    weeks = season.gameweek_set.all()

    ret = {}

    #wins, losses, games for, games against, goals for, goals against
    for w in weeks:
        games = w.game_set.all()
        print(games)
        week_res = {}
        
        for g in games:
            if g.home_team.key not in ret.keys():
                ret[g.home_team.key] = {'name':g.home_team.name,'wins':0,'losses':0,'for':0,'against':0,'goals_for':0,'goals_against':0}
            if g.away_team.key not in ret.keys():
                ret[g.away_team.key] = {'name':g.away_team.name,'wins':0,'losses':0,'for':0,'against':0,'goals_for':0,'goals_against':0}
            if g.home_team.key not in week_res.keys():
                week_res[g.home_team.key] = 0
            if g.away_team.key not in week_res.keys():
                week_res[g.away_team.key] = 0
            winner = ''
            loser = ''
            if g.outcome == g.home_team.key:
                week_res[g.home_team.key] += 1
                winner = 'ht'
                loser = 'at'
            else:
                week_res[g.away_team.key] += 1
                winner = 'at'
                loser = 'ht'
            if winner == 'ht':
                ret[g.home_team.key]['for']+=1
                ret[g.away_team.key]['against']+=1
            else:
                ret[g.home_team.key]['against']+=1
                ret[g.away_team.key]['for']+=1
                
            ret[g.home_team.key]['goals_for']+=g.home_team_score
            ret[g.home_team.key]['goals_against']+=g.away_team_score

            ret[g.away_team.key]['goals_for']+=g.away_team_score
            ret[g.away_team.key]['goals_against']+=g.home_team_score
            
            if week_res[g.away_team.key] + week_res[g.home_team.key] == 3:
                if week_res[g.home_team.key] > week_res[g.away_team.key]:
                    ret[g.home_team.key]['wins']+=1
                    ret[g.away_team.key]['losses']+=1
                else:
                    ret[g.home_team.key]['losses']+=1
                    ret[g.away_team.key]['wins']+=1
            print(week_res)


    output = []
    for k in ret.keys():
        outlist = [ret[k]['name'],ret[k]['wins'],ret[k]['losses'],ret[k]['for'],ret[k]['against'],ret[k]['goals_for'],ret[k]['goals_against']]
        output.append(outlist)
    print(output)
    output = sorted(output,key=lambda l:l[1],reverse=True)
    print(output)
    return render(request,'stats/season.html',{'season':season,'weeks':weeks,'games':games,'table':output})

def week(request,season_slug,week_number):
    season = get_object_or_404(Season,slug=season_slug)
    week = get_object_or_404(GameWeek,season=season,number=week_number)
    games = week.game_set.all().order_by('series_number')
    return render(request,'stats/week.html',{'season':season,'week':week,'games':games})

def table(request):
    #need all
    pass

def game(request,season_slug,week_number,ht,at,series_number):
    season = get_object_or_404(Season,slug=season_slug)
    week = get_object_or_404(GameWeek,season=season,number=week_number)
    home = get_object_or_404(Team,key=ht)
    away = get_object_or_404(Team,key=at)
    game = get_object_or_404(Game,gameweek=week,series_number=series_number,home_team=home,away_team=away)
    gs = game.gamestats_set.all()
    rdict = {}
    rdict['season'] = season
    rdict['week'] = week
    rdict['game'] = game
    rdict['stats'] = gs
    return render(request,'stats/game.html',rdict)
