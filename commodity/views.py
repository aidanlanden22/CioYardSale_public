from django.shortcuts import render
from .forms import CommodityForm, CommodityPicForm
from .models import Commodity
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from django.core import serializers
import json

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

# ********** THIS IS THE API FOR COMMODITIES **********
def read(request, pk):
    # Format the JSON Response for a GET Request
    if request.method == 'GET':
        # Imported from django
        # Gives you model, pk, fields - user, year

        data = serializers.serialize("json", Commodity.objects.filter(id=pk))
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def create(request):
    #if request.method == 'POST':


    if request.method == 'POST':
        form = CommodityForm(request.POST)
        print("hey334")
        if form.is_valid():

            selling = Commodity.objects.create(
                g_or_s=form.cleaned_data['g_or_s'],
                quantity=form.cleaned_data['quantity'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                date_expires=form.cleaned_data['date_expires'],
                title=form.cleaned_data['title'],
                cio=request.user
            )

            selling.save()

            data = serializers.serialize("json", [selling])
            return HttpResponse(data, content_type='application/json')
