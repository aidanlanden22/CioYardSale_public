from django import forms
from django.contrib.auth.models import User


# Form for CIOs - the built in User fields
class SignUpCio(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.CharField(widget=forms.EmailInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)



# Add a picture to a commodity
class CommodityPicForm(forms.Form):
    picture = forms.ImageField()


# Form for students - the built in User fields
class SignUpUser(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(widget=forms.EmailInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

# Login a user
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['password'].widget.attrs = {
            'class': 'form-control'
        }
