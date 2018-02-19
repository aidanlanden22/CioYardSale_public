from django import forms
from django.contrib.auth.models import User
from .models import Cio

# Form for the built in User fields
class SignUpCio(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.CharField(widget=forms.EmailInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    # Use to format and style the form
    def __init__(self, *args, **kwargs):
        super(SignUpUser, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['password'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['email'].widget.attrs = {
            'class': 'form-control'
        }

    # Emails for each user should be unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'That email address is already taken.')
        return email

    class Meta:
        model = User
        fields = ['username','password','email']

