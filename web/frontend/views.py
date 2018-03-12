from django.shortcuts import render

from . import forms

import urllib.request
import urllib.parse
import json

def index(request):
    req = urllib.request.Request('http://exp-api:8002/getCommodityList/')
    json_response = urllib.request.urlopen(req).read().decode('utf-8')
