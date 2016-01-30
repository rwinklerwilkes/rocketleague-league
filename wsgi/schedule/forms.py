from django import forms
from django.contrib.auth.models import User
from stats.models import Player
from PIL import Image

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=User
        fields=('username','email','password')

class UserChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),label='Current Password (Required)')
    new_pass1 = forms.CharField(widget=forms.PasswordInput(),label='New Password')
    new_pass2 = forms.CharField(widget=forms.PasswordInput(),label='Confirm New Password')

    def clean(self):
        if 'new_pass1' in self.cleaned_data and 'new_pass2' in self.cleaned_data:
            if self.cleaned_data['new_pass1'] != self.cleaned_data['new_pass2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

    class Meta:
        model=User
        fields=('email','password','new_pass1','new_pass2')

class PlayerForm(forms.ModelForm):
    class Meta:
        model=Player
        fields=('player_first_name','player_last_name','player_nickname','player_team')

class ProfilePicForm(forms.ModelForm):
    def clean_profile_pic(self):
        image = self.cleaned_data['profile_pic']
        if image:
            img = Image.open(image)
            if img.width*img.height > 250*250:
                raise ValidationError("Image too large (250px by 250px max)")
        else:
            raise ValidationError("Couldn't read uploaded image")
        return image
    
    class Meta:
        model=Player
        fields=('profile_pic',)
