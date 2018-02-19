
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from .forms import SignUpCio
from .models import Cio

from django.core import serializers
import json

def profile(request):
    myKey = request.user.id
    return render(request, 'cio/profile.html', {'myKey': myKey })

def signup(request):
    if request.user.is_authenticated and Cio.objects.filter(user=request.user).exists():
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        cioForm = SignUpCio(request.POST)
        formErrors = {}
        formErrors.update(cioForm.errors)
        if cioForm.is_valid():
            cio = User.objects.create_user(
                username=cioForm.cleaned_data['username'],
                password=cioForm.cleaned_data['password'],
                email=cioForm.cleaned_data['email']
            )
            cio.save()
            login(request, cio)
            return HttpResponseRedirect(reverse('cio:profile'))

        return render(request, 'cio/signup.html', {'errors': formErrors,  'cioForm': cioForm})

    cioForm = SignUpCio()
    return render(request, 'cio/signup.html', {'cioForm': cioForm})

def logoutUser(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect(reverse('index'))

# ********** THIS IS THE API FOR CIOs **********
def read(request, pk):
    # Format the JSON Response for a GET Request
    if request.method == 'GET':
        # Imported from django
        # Gives you model, pk, fields - user, year
        data = serializers.serialize("json", User.objects.filter(id=pk), fields=('username', 'email', 'date_joined'))

    # Format the JSON Response for a POST Request
    elif request.method == 'POST':
        # TO DO
        response = JsonResponse({'foo': 'buzz'})
    return HttpResponse(data, content_type='application/json')

def create(request):
    data = {}
    if request.method == 'GET':
        status = {'status': 'unsucessful request'}
        data = json.dumps(status)
    elif request.method == 'POST':
        # TO DO: check if the username already exists
        try:
            myUser = User.objects.create_user(
                username = request.POST.get('username'),
                email = request.POST.get('email'),
                password = hashers.make_password(request.POST.get('password'))
            )
            myUser.save()
            
        except Exception as e:
            return JsonResponse({'status': str(e)})
    return HttpResponse(data, content_type='application/json')

def update(request, pk):
    data = {}
    if request.method == 'GET':
        status = {'status': 'unsucessful request'}
        data = json.dumps(status)
    elif request.method == 'POST':
        try:
            user = User.objects.get(id=pk)
        except Exception as e:
            return JsonResponse({'status': str(e)})
        status = {'status': 'unsucessful request', 'action': 'nothing updated'}
        if request.POST.get('username'):
            user.username = request.POST.get('username')
            user.save()
            status = {'status': 'sucessful request', 'action': 'updated username'}
        if request.POST.get('email'):
            user.email = request.POST.get('email')
            user.save()
            status = {'status': 'sucessful request', 'action': 'updated email'}
        if request.POST.get('password'):
            user.password = hashers.make_password(request.POST.get('password'))
            user.save()
            status = {'status': 'sucessful request', 'action': 'updated password'}
        response = {'first name': user.first_name,'last name': user.last_name,
                'username': user.username, 'email': user.email}
        full_response = {'status': status, 'response': response}
        data = json.dumps(full_response)

    return HttpResponse(data, content_type='application/json')


def delete(request, pk):
    data = {}
    if request.method == 'GET':
        status = {'status': 'unsucessful request'}
        data = json.dumps(status)
    elif request.method == 'POST':
        user = User.objects.filter(id=pk)
        user.delete()
        status = {'status': 'sucessful request', 'action': 'deleted user'}
        data = json.dumps(status)
    return HttpResponse(data, content_type='application/json')
