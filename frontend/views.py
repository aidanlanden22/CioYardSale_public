from django.shortcuts import render

from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login, logout

from api.commodity.forms import CommodityForm

def index(request):
    return render(request, 'index.html')

def sellItem(request):
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
    else:
        form = CommodityForm()
    return render(request, 'commodity/createcommodity.html', {'form': form})

def CioProfile(request):
    myKey = request.user.id
    return render(request, 'cio/profile.html', {'myKey': myKey })
