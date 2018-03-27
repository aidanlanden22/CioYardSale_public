from django.shortcuts import render
from .forms import *

from . import forms

import urllib.request
import urllib.parse
import json

def index(request):
    req = urllib.request.Request('http://exp-api:8000/getCommodityList/')
    print(req)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    context = {
        'items': resp,
    }

    return render(request, 'index.html', context)

def view_item(request, pk):
    context = {'pk' : pk}
    req = urllib.request.Request('http://exp-api:8000/getSingleCommodity/' + pk + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)



    context = {
        'pk' : pk,
        'item': resp[0],
    }

    return render(request, 'item.html',context)

def register_student(request):
    form = RegisterStudent
    if request.method == 'POST':
        form = RegisterStudent(request.POST)
        if form.is_valid():
            data = {'username': form.cleaned_data['username'],
                         'password': form.cleaned_data['password'],
                         'year': form.cleaned_data['year']}
            data_encoded = urllib.parse.urlencode(data).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/registerStudent/', data=data_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)

            #check if username is alreadyy taken

            #auth = resp['auth']['auth']
            #response = HttpResponseRedirect(reverse('home'))
            #response.set_cookie("auth", auth)
            #response.set_cookie("user", form.cleaned_data['username'])
            #return response
        return render(request, 'signup.html', {'form': form, 'message': form.errors})
    else:
        return render(request, 'signup.html', {'form': form})