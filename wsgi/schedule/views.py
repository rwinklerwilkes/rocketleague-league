from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    
    user = authenticate(username=username,password=password)

    if user is not None:
        #valid, log in
        login(request,user)
    else:
        #invalid
        pass
