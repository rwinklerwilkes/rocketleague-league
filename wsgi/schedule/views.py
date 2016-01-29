from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from schedule.forms import UserForm, PlayerForm
from stats.models import Player, GameStats, Game, Season, GameWeek
import json

def register(request):
    #will set to true if registration is successful
    registered = False

    #posted, so we'll check the data
    if request.method == 'POST':
        #take post information and put into forms
        user_form = UserForm(data=request.POST)
        player_form = PlayerForm(data=request.POST)

        if user_form.is_valid() and player_form.is_valid():
            #make a new user
            user = user_form.save()
            
            #set the password
            user.set_password(user.password)
            user.save()

            #now work with the player
            #we need to add the user attribute to the player, so we don't commit yet
            player = player_form.save(commit=False)
            player.user = user

            player.save()

            registered = True

        #invalid form or forms
        else:
            print(user_form.errors)
            print(player_form.errors)

    #not a post request
    #so, render page with two instances - these will be blank for input
    else:
        user_form = UserForm()
        player_form = PlayerForm()

    return render(request,'schedule/register.html',{'user_form':user_form,'player_form':player_form,'registered':registered})
    

def vw_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/schedule/main/')
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(username=username,password=password)

    if user is not None:
        #valid, log in
        if user.is_active:
            login(request,user)
            return HttpResponseRedirect('/schedule/main/')
    else:
        #invalid, redirect to login site
        return render(request,'schedule/login.html')

@login_required
def main(request):
    user = request.user
    #which player is the user?
    player = user.player
    player.update_stats()
    #what are their stats?
    gs = GameStats.objects.filter(player=player)

    seasons = []
    weeks = []
    #get unique seasons and weeks
    for row in gs:
        cur_w = row.game.gameweek.number
        if cur_w not in weeks:
            weeks.append(cur_w)
        cur_s = row.game.gameweek.season.slug
        if cur_s not in seasons:
            seasons.append(cur_s)
    sorted(weeks)
    sorted(seasons)
    
    return render(request,'schedule/main.html',{'stats':gs,'player':player,'user':user,'weeks':weeks,'seasons':seasons})

@login_required
def chart_data(request):
    if request.method == 'GET':
        player = request.user.player
        gs = GameStats.objects.filter(player=player)
        season = request.GET['season']
        week = request.GET['week']
        out = request.GET['out']

        if season != 'All':
            getstats = [g for g in gs if g.game.gameweek.season.slug == season]

        if week != 'All':
            getstats = [g for g in getstats if g.game.gameweek.number==week]

        #use getattr to get the stat that we care about
        returnstats = []
        returnstats.append(['Week',out])
        for gsrow in getstats:
            cur_it = []
            cur_it.append(str(gsrow.game.gameweek.number) + str(gsrow.game.series_number))
            cur_it.append(getattr(gsrow,out))
            returnstats.append(cur_it)

        rdict = {'stats':returnstats}

    else:
        rdict = {'stats':[]}
    return JsonResponse(rdict)

def vw_logout(request):
    logout(request)
    return HttpResponseRedirect('/') 
