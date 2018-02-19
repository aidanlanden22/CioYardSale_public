from django.shortcuts import render
from .forms import CommodityForm, CommodityPicForm
from .models import Commodity
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

# Create your views here.
def sell(request):
    if request.method == 'POST':
        form = CommodityForm(request.POST)
   
        if form.is_valid():
            selling = Commodity.objects.create(
                g_or_s=form.cleaned_data['g_or_s'],
                quantity=form.cleaned_data['quantity'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                date_expires=form.cleaned_data['date_expires'],
                title=form.cleaned_data['title']
            )
            selling.save()
            
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommodityForm()

    return render(request, 'createcommodity.html', {'form': form})