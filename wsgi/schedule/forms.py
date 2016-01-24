from django import forms
from django.contrib.auth.models import User
from stats.models import Player

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=User
        fields=('username','email','password')

class PlayerForm(forms.ModelForm):
    class Meta:
        model=Player
        fields=('player_first_name','player_last_name','player_nickname','player_team')
