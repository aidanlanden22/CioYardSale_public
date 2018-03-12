from django.shortcuts import render

from . import forms

import urllib.request
import urllib.parse
import json

def index(request):
    req = urllib.request.Request('http://exp-api:8000/api/v1/experience/getCommodityList/')
    # json_response = urllib.request.urlopen(req).read().decode('utf-8')
    # response = json.loads(json_response)
    # items = json.loads(response)

    context = {
        'items' : [],
        'req' : req,
    }

    return render(request, 'index.html', context)
