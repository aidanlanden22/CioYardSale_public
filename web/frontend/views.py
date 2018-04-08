from django.shortcuts import render
from .forms import *
from django.core.urlresolvers import reverse

from . import forms

from django.http import JsonResponse, HttpResponseRedirect

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
                # 'date_expires' : form.cleaned_data['date_expires']
            }

            data_encoded = urllib.parse.urlencode(data).encode('utf-8')
            req = urllib.request.Request('http://exp-api:8000/createCommodity/', data=data_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
            if not resp['status'] == 'success':
                if resp['response']:
                    response = HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing"))
                    response.delete_cookie('auth')
                    response.delete_cookie('user')
                    return response
                else:
                    return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing"))
            return index(request)
        else:
            return JsonResponse({'status': 'error', 'response': form.errors})

    return render(request, 'index.html')


        #template_name = 'templates/commodity/createcommodity.html'

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

    # if request.method == 'GET':
    #     if request.COOKIES.get('auth'):
    #         json_response = {
    #             'status': 'error',
    #             'response': "Received a GET request. Expected a POST request.",
    #             'data': data,
    #             'auth': request.COOKIES.get('auth'),
    #         }
    #         return JsonResponse(json_response)
    #     json_response = {
    #         'status': 'error',
    #         'response': "Received a GET request. Expected a POST request. No Auth token.",
    #         'data': data,
    #         'auth': request.COOKIES.get('auth'),
    #     }
    #     return JsonResponse(json_response)

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
