from django.shortcuts import render
from .forms import *

from . import forms

from django.http import JsonResponse, HttpResponseRedirect

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

    if not resp or not resp['resp'] or resp['resp']['status']=='error':
        return render(request, 'login.html', {'login_form': login_form, 'message': 'User could not be logged in'})

    auth = resp['resp']['auth']
    response = HttpResponseRedirect(next)
    response.set_cookie("auth", auth)
    response.set_cookie("user", login_form.cleaned_data['username'])
    return response


# Log out the current user
def logout(request):
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
    except:
        return JsonResponse({'status': 'error'})
    return response
