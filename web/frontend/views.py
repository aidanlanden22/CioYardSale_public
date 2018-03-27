from django.shortcuts import render
from .forms import *

from . import forms

import urllib.request
import urllib.parse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect

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


def create_listing(request):

    # Try to get the authenticator cookie
    auth = request.COOKIES.get('auth')

    if not auth: 

        return HttpResponseRedirect(reverse("login") + "?next=" + reverse("createcommodity")

    if request.method = 'GET':
        form = CreateCommodityForm()
        return render(request, 'commodity/createcommodity.html', {'form': form, 'created' : false})

    if request.method == 'POST':
        form = CreateCommodityForm(request.POST)
        if form.is_valid():
            post_data = {
                'g_or_s' : form.cleaned_data['g_or_s'],
                'title' : form.cleaned_data['title'],
                'description' : form.cleaned_data['description'],
                'price' : form.cleaned_data['price'],
                'quantity' : form.cleaned_data['quantity']
            }

            post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

            req = urllib.request.Request('http://exp-api:8000/api/v1/create/', data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
            if not resp['status'] == 'success':
                if resp['response']:
                    response = HttpResponseRedirect(reverse("login") + "?next=" + reverse("createcommodity"))
                    response.delete_cookie('auth')
                    response.delete_cookie('user')
                    return response
                else:
                    return HttpResponseRedirect(reverse("login") + "?next=" + reverse("createcommodity"))
            return index(request)
        else: 
            return JsonResponse({'status': 'error', 'response': form.errors})

    return render(request, 'index.html')



@csrf_exempt
def signup_user(request):
    form = RegisterUser
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            data = {'username': form.cleaned_data['username'],
                         'password': form.cleaned_data['password'],
                         #'year': form.cleaned_data['year']
                }
            data_encoded = urllib.parse.urlencode(data).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/signupUser/', data=data_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
            #if resp['response'] == 'Username already exists.':
            #    return resp

            return HttpResponseRedirect('/')
        return render(request, 'signup.html', {'form': form, 'message': form.errors})
    else:
        return render(request, 'signup.html', {'form': form})

