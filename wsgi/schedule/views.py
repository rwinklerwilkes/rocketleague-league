from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from schedule.forms import UserForm, PlayerForm, ProfilePicForm, UserChangeForm
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

#this function will handle 3 forms
#merge into main so user can change stuff from main page
#profile pic form, user change form, and player form
@login_required
def user_profile_change(request):
    if request.method == 'POST':
        ucform = UserChangeForm(data=request.POST,instance=request.user)
        pform = PlayerForm(data=request.POST,instance=request.user.player)
        picform = ProfilePicForm(request.POST,request.FILES,instance=request.user.player)

        if ucform.is_valid():
            oldpass = ucform.cleaned_data['password']
            newpass = ucform.cleaned_data['new_pass1']
            user = authenticate(username=request.user.username,password=oldpass)

            if user is not None:
                if picform.is_valid():
                    picform.save()
                if pform.is_valid():
                    pform.save()
                if newpass is not None:
                    user.set_password(newpass)
                    user.save()
                user.email = ucform.cleaned_data['email']
    else:
        picform = ProfilePicForm(instance=request.user.player)
        pform = PlayerForm(instance=request.user.player)
        ucform = UserChangeForm(instance=request.user)

    return render(request,'schedule/edit_profile.html',{'user_form':ucform,'player_form':pform,'pic_form':picform})
        

@login_required
def main(request):  
    user = request.user
    #which player is the user?
    player = user.player
    player.update_stats()

    if request.method == 'POST':
        if 'picsubmit' in request.POST:
            pic_form = ProfilePicForm(request.POST, request.FILES,instance=request.user.player)

            if pic_form.is_valid():
                p = pic_form.save()
    else:
        pic_form = ProfilePicForm(instance=request.user.player)
    
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
    
    return render(request,'schedule/main.html',{'stats':gs,'player':player,'user':user,'weeks':weeks,'seasons':seasons,'pic_form':pic_form})

@login_required
def chart_data(request):
    if request.method == 'GET':
        player = request.user.player
        gs = GameStats.objects.filter(player=player)
        getstats = gs
        season = request.GET['season']
        #it will either be converted to an int or I'll grab all of them instead
        try:
            week = int(request.GET['week'])
        except:
            week = 'All'
        #out should be of the form [goals,assists,saves,shots,points]
        #will be a 1 if wanted, 0 if not
        out = [int(i) for i in request.GET['out'].split(',')]
        out_list = ['goals','assists','saves','shots','points']

        if season != 'All':
            getstats = [g for g in gs if g.game.gameweek.season.slug == season]

        if week != 'All':
            getstats = [g for g in getstats if g.game.gameweek.number==week]

        #use getattr to get the stat that we care about
        returnstats = []
        legend = ['Week'] + [out_list[i] for i in range(len(out)) if out[i]==1]
        returnstats.append(legend)
        for gsrow in getstats:
            cur_it = []
            cur_it.append('Week ' + str(gsrow.game.gameweek.number) + ' Game ' + str(gsrow.game.series_number))

            for i in range(len(out)):
                if out[i]==1:
                    cur_it.append(getattr(gsrow,out_list[i]))
            returnstats.append(cur_it)

        rs_test = len(returnstats[0])
        for i in returnstats:
            assert len(i)==rs_test

        rdict = {'stats':returnstats}

    else:
        rdict = {'stats':[]}
    return JsonResponse(rdict)

def vw_logout(request):
    logout(request)
    return HttpResponseRedirect('/') 
