from .forms import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from . import forms

import json
from django.http import JsonResponse, HttpResponseRedirect

import requests
import urllib.request
import urllib.parse

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

def search(request):
    if request.method == 'GET':
        # 'query' is the name field in the search input in base.html
        data = request.GET.get('query')

        # Send the query to the exp url and store info in resp
        resp = requests.get('http://exp-api:8000/api/v1/search/', params={'query': data})

        # Get the actual text of the resp
        resp_json = resp.text

        if json.loads(resp_json)['response'] == 'Found items':
            items = json.loads(resp_json)['items']
            return render(request, 'search_results.html', {'items': items})

        else:
            return render(request, 'search_results.html', {'items': None})
    else:
        json_response = {
            'status': 'error',
            'response': 'Expected a GET request. Received a POST request.',
        }
        return JsonResponse(json_response)

@csrf_exempt
def create_listing(request):

    # Try to get the authenticator cookie
    auth = request.COOKIES.get('auth')

    if not auth:
        return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing"))

    if request.method == 'GET':
        form = CreateCommodityForm()
        return render(request, 'commodity/createcommodity.html', {'form': form, 'created' : False})

    if request.method == 'POST':
        form = CreateCommodityForm(request.POST)
        if form.is_valid():
            data = {
                'g_or_s' : form.cleaned_data['g_or_s'],
                'title' : form.cleaned_data['title'],
                'description' : form.cleaned_data['description'],
                'price' : form.cleaned_data['price'],
                'quantity' : form.cleaned_data['quantity'],
                'date_expires' : '2012-09-04 06:00:00.000000-08:00',
            }

            data_encoded = urllib.parse.urlencode(data).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/createCommodity/', data=data_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)

            if resp:
                return HttpResponseRedirect('/')
            else:
                return JsonResponse({'status': 'error', 'response': 'Did not get a response'})
        else:
            return JsonResponse({'status': 'error', 'response': 'Form input invalid', 'Errors': form.errors})

    return HttpResponseRedirect('/')

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
            if resp['response'] == 'Username already exists.':
                return render(request, 'signup.html', {'form': form, 'message': "Error: User with that username already exists."})
            login(request)
            return HttpResponseRedirect('/')
        return render(request, 'signup.html', {'form': form, 'message': form.errors})
    else:

        return render(request, 'signup.html', {'form': form})

# Log in a user
def login(request):
    login_form = LoginForm()

    if request.method == 'GET':
        if request.COOKIES.get('auth'):
            return render(request, 'login.html', {'logged_in': 'you are logged in'})
        return render(request, 'login.html', {'login_form': login_form})

    login_form = LoginForm(request.POST)

    if not login_form.is_valid():
        return render(request, 'login.html', {'login_form': login_form, 'message': login_form.errors})

    post_data = {
        'username': login_form.cleaned_data['username'],
        'password': login_form.cleaned_data['password']
    }

    next = request.GET.get('next') or reverse('index')
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/api/v1/login/', data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['resp']['status']=='error':
        return render(request, 'login.html', {'login_form': login_form, 'message': resp['resp']['response'] })

    auth = resp['resp']['auth']
    response = HttpResponseRedirect(next)
    response.set_cookie("auth", auth)
    response.set_cookie("user", login_form.cleaned_data['username'])
    return response


# Log out the current user
def logout(request):
    data = {}

    try:
        authenticator = request.COOKIES['auth']
        data = {'auth': authenticator}
        data_encoded = urllib.parse.urlencode(data).encode('utf-8')

        # Make a call to the Experience layer (8000)
        req = urllib.request.Request('http://exp-api:8000/api/v1/logout/', data=data_encoded, method='POST')

        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)

        response = HttpResponseRedirect('/login')
        response.delete_cookie('auth')
        response.delete_cookie('user')
    except Exception as e:
        json_response = {
            'status': 'error',
            'response': e.read(),
            'data': data,
        }
        return JsonResponse(json_response)
    return response
