from django.shortcuts import render

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