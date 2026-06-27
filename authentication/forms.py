from django import forms
from django.contrib.auth import authenticate

class Loginform(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

    def authenticate_user(self):
        user=authenticate(username=self.cleaned_data['username'],
                          password=self.cleaned_data['password'])
        return user
    
