from django import forms

class LogInUser(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LogInUser, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['password'].widget.attrs = {
            'class': 'form-control'
        }
