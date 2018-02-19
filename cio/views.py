
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
        data = serializers.serialize("json", Cio.objects.filter(id=pk))

    # Format the JSON Response for a POST Request
    elif request.method == 'POST':
        # TO DO
        response = JsonResponse({'foo': 'buzz'})
    return HttpResponse(data, content_type='application/json')
