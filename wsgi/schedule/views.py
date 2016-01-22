from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

def login(request):
    #get
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(username=username,password=password)

    if user is not None:
        #valid, log in
        login(request,user)
        return HttpResponseRedirect('/main/')
    else:
        #invalid, redirect to login site
        return render(request,'schedule/login.html')

def main(request):
    return render(request,'schedule/main.html')
