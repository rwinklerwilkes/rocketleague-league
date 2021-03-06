from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Player, Team, Season, GameWeek
from .models import Game, GameStats
import json

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
        #print(games)
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
            #print(week_res)


    output = []
    for k in ret.keys():
        outlist = [ret[k]['name'],ret[k]['wins'],ret[k]['losses'],ret[k]['for'],ret[k]['against'],ret[k]['goals_for'],ret[k]['goals_against']]
        output.append(outlist)
    #print(output)
    output = sorted(output,key=lambda l:l[1],reverse=True)
    #print(output)

    games = {}
    #get the week:game mapping
    for w in weeks:
        games[str(w.number)] = sorted(w.game_set.all(),key=lambda x: (x.home_team.name,x.away_team.name,x.series_number))
    
    return render(request,'stats/season.html',{'season':season,'weeks':weeks,'games':games,'table':output})

def week(request,season_slug,week_number):
    season = get_object_or_404(Season,slug=season_slug)
    week = get_object_or_404(GameWeek,season=season,number=week_number)
    games = week.game_set.all().order_by('series_number')
    return render(request,'stats/week.html',{'season':season,'week':week,'games':games})

def teams(request):
    #hard code current season
    season = get_object_or_404(Season,slug='201601')
    teams_in_season = {}

    weeks = GameWeek.objects.filter(season=season)
    games = []
    week_set = []
    for w in weeks:
        games += [g for g in Game.objects.filter(gameweek=w)]

    for g in games:
        cur_week_key = str(g.gameweek.number)+str(g.series_number)
        #g is a single game
        if g.home_team not in teams_in_season.keys():
            teams_in_season[g.home_team.key] = {'name':g.home_team.name,cur_week_key:g.home_team_score}
        else:
            teams_in_season[g.home_team.key][cur_week_key]=g.home_team_score
        if g.away_team not in teams_in_season.keys():
            teams_in_season[g.away_team.key] = {'name':g.away_team.name,cur_week_key:g.away_team_score}
        else:
            teams_in_season[g.away_team.key][cur_week_key]=g.away_team_score
        if cur_week_key not in week_set:
            week_set.append(cur_week_key)

    sorted(week_set)

    #teams_in_season now has all of the teams and their weekly scores
    #have to get player set
    p = Player.objects.all()
    for player in p:
        try:
            cur_t = player.player_team.key
            if cur_t in teams_in_season.keys():
                try:
                    teams_in_season[cur_t]['players'].append(player)
                except:
                    teams_in_season[cur_t]['players']=[player]
        except:
            pass
    keys = teams_in_season.keys()

    return render(request,'stats/teams.html',{'teams':teams_in_season,'weeks':week_set,'keys':keys})

def team_data(request):
    if request.method == 'GET':
        season_slug = request.GET['season']
        team_key = request.GET['team']
        t = get_object_or_404(Team,key=team_key)
        s = Season.objects.get(slug=season_slug)
        #get all objects for players on t in season s
        gs = GameStats.objects.filter(player__player_team=t,game__gameweek__season=s)

        
        #copied from other chart data view
        #out will be of the form 1,1,1,0,1
        out = [int(i) for i in request.GET['out'].split(',')]
        return_stats = {}
        out_list = ['goals','assists','saves','shots','points']
        legend =['Week'] + [out_list[i] for i in range(len(out)) if out[i]==1]
        for g in gs:
            key = 'Week ' + str(g.game.gameweek.number) + ' Game ' + str(g.game.series_number)
            #an earlier teammate hasn't been seen (first time we've seen this week)
            if key not in return_stats:
                #add the key
                return_stats[key] = [0 for i in range(len(out))]
            for i in range(len(out)):
                if out[i]==1:
                    return_stats[key][i]+=getattr(g,out_list[i])
            
        #so, return_stats should now look like {'Week 1 Game 1':[3,2,0,8,1500],...}
        #going to put it in a similar form to the other output from the other chart view (in schedule)
        return_stats_list = [legend]
        for k,v in return_stats.items():
            cur_list = v
            #fix the list, since we may not want all of the items
            fixed_list = [cur_list[i] for i in range(len(out)) if out[i] > 0]
            fixed_list.insert(0,k)
            return_stats_list.append(fixed_list)

        return_stats_list_sorted = [legend]
        return_stats_list_sorted += sorted(return_stats_list[1:],key=lambda x:x[0])

        rdict = {'stats':return_stats_list_sorted}

    else:
        rdict = {'stats':[]}
    return JsonResponse(rdict)
        
            
            

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
