from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

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
    return render(request,'schedule/main.html')

def vw_logout(request):
    logout(request)
    return HttpResponseRedirect('/') 
