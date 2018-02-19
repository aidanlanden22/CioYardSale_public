from django import forms
from .models import Commodity

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
        exclude = ['date_created','picture']

class CommodityPicForm(forms.Form):
    picture = forms.ImageField()
    
    def __init__(self, *args, **kwargs):
        super(CommodityPicForm, self).__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs = {
            'class': 'form-control'
        }

    class Meta:
        model = Commodity
        exclude = ['date_created','g_or_s','title','description','quantity','price','date_expires']