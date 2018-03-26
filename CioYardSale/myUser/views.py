from django.shortcuts import render
from django.contrib.auth import hashers

# Grab the models we made in this myUser application
from .models import myUser, Authenticater

# From the Project 4 documentation
import os
import hmac
from CioYardSale import settings     # import django settings file

from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import hashers
from django.http import JsonResponse
import json

#   Create the signup view
#   creates a new user when they signup
#
@csrf_exempt
def create_user(request):
    data = {}
    if request.method == 'GET':
        status = {'status': 'unsuccessful request'}
        data = json.dumps(status)
    elif request.method == 'POST':
        if myUser.objects.filter(username=request.POST.get('username')):
            status = ({'status': 'unsuccessful request','response':'username already exists'})
            data = json.dumps(status)
        try:
            user = myUser.objects.create(
                username = request.POST.get('username'),
                password = hashers.make_password(request.POST.get('password'))
            )
            user.save()
            status = ({'status': 'user created successfully', 'response':{'username':user.username}})
            data = json.dumps(status)
            return HttpResponse(data, content_type='application/json')
        except Exception as e:
            return JsonResponse({'status': str(e)})
    return HttpResponse(data, content_type='application/json')

#   Create the login view
#
#   needs to take in the username and password and authenticate the user
#   if the user is ok, return an authenticator back to the experience service
#
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = myUser.objects.get(username=username)
            # Use hashers to check the password
            if hashers.check_password(password, user.password):
                #
                create_auth(request)
                auth = (Authenticator.objects.get(user=user))
                return JsonResponse({'status': 'success','auth':auth.authenticator},safe=False)
            else:
                return JsonResponse({'status': 'error','response':'Incorrect Password'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error','response':'User does not exist'})
    return JsonResponse({'status': 'error','response':'POST expected, GET found'})


#   Create an authenticater
#
#   uses the instructions in the Project 4 documentation
#   will make a new authenticater
#
@csrf_exempt
def create_auth(request):
    if request.method == 'POST':

        # From the Project 4 documentation
        authenticater = hmac.new(
            key=settings.SECRET_KEY.encode('utf-8'),
            msg=os.urandom(32),
            digestmod='sha256',
        ).hexdigest()

        try:
            user = myUser.objects.get(username=request.POST.get('username'))
            auth = Authenticator(
                user = user,
                authenticater = authenticater,
            )
            auth.save()
            return JsonResponse({'status':'success', 'user':auth.user.username, 'auth':auth.authenticator,
                                 'date_created':auth.date_created})
        except Exception as e:
            return JsonResponse({'status': str(e)})
    return JsonResponse({'status': 'Error: must make POST request'})


def readAll(request):
    if request.method == 'GET':
        data = serializers.serialize("json", myUser.objects.all())
        return HttpResponse(data, content_type='application/json')

    if request.method == 'POST':
        status = {'status': 'unsucessful request'}
        data = json.dumps(status)
        return HttpResponse(data, content_type='application/json')



