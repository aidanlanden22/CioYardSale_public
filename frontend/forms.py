from django import forms
from django.contrib.auth.models import User

from api.cio.models import Cio
from api.students.models import Student
from api.commodity.models import Commodity


# Form for CIOs - the built in User fields
class SignUpCio(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.CharField(widget=forms.EmailInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    # Use to format and style the form
    def __init__(self, *args, **kwargs):
        super(SignUpCio, self).__init__(*args, **kwargs)
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

# Form to make a new commodity
class CommodityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommodityForm, self).__init__(*args, **kwargs)

        self.fields['g_or_s'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['title'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['description'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['quantity'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['price'].widget.attrs = {
            'class':'form-control'
        }
        self.fields['date_expires'].widget.attrs = {
            'class': 'form-control'
        }

    class Meta:
        model = Commodity
        exclude = ['date_created','picture','id']

# Add a picture to a commodity
class CommodityPicForm(forms.Form):
    picture = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CommodityPicForm, self).__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs = {
            'class': 'form-control'
        }

    class Meta:
        model = Commodity
        exclude = ['date_created','g_or_s','title','description','quantity','price','date_expires','id']

# Form for students - the built in User fields
class SignUpUser(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
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
        self.fields['first_name'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['last_name'].widget.attrs = {
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
        fields = ['username','password','first_name','last_name','email']

# Form for the additional User fields
class SignUpStudent(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignUpStudent, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs = {
            'class': 'form-control'
        }

    class Meta:
        model = Student
        exclude = ['active','user']

# Let the user edit their profile
class EditUser(forms.ModelForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(widget=forms.EmailInput, required=True)

    def __init__(self, *args, **kwargs):
        super(EditUser, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['first_name'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['last_name'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['email'].widget.attrs = {
            'class': 'form-control'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.instance.username
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'That email address is already taken.')
        return email

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
