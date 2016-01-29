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

class ProfilePicForm(forms.ModelForm):
    def clean_profile_pic(self):
        image = self.cleaned_data.get('profile_pic',False)
        if image:
            if image.width*image.height > 250*250:
                raise ValidationError("Image too large (250px by 250px max)")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")
    
    class Meta:
        model=Player
        fields=('profile_pic')
