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

# Form for CIO's to list a new commodity
class CreateCommodityForm(forms.ModelForm):
	GOOD_OR_SERVICE = (
    ('G', 'Good'),
    ('S', 'Service'),
    )
	g_or_s = forms.CharField(max_length=1, choices=GOOD_OR_SERVICE, default='G')
	title = forms.CharField(required=True)
	price = forms.DecimalField(max_digits=6, decimal_places=2)
	description = forms.CharField(required=True)
	quantity = forms.IntegerField(required=True)

