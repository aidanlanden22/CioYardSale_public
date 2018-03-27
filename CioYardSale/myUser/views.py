from django.shortcuts import render
from django.core import serializers
from django.contrib.auth import hashers
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json

from .models import myUser, Authenticater

import os
import hmac
from CioYardSale import settings

#   Create the signup view
#   creates a new user when they signup
#
@csrf_exempt
def create_user(request):
    json_response = {}
    if request.method == 'GET':
        json_response = {
            'status': 'error',
            'response': 'POST request expected. GET request found.',
        }
        return JsonResponse(json_response)

    if request.method == 'POST':
        if myUser.objects.filter(username=request.POST.get('username')):
            status = ({'status': 'unsuccessful request','response':'username already exists'})
            json_response = {
                'status': 'error',
                'response': 'Username already exists.',
            }
            return JsonResponse(json_response)

        try:
            user = myUser.objects.create(
                username = request.POST.get('username'),
                password = hashers.make_password(request.POST.get('password'))
            )
            user.save()
            json_response = {
                'status': 'success',
                'response': {
                    'username': user.username,
                }
            }
            return JsonResponse(json_response)

        except Exception as e:
            json_response = {
                'status': 'error',
                'response': str(e),
            }
            return JsonResponse(json_response)
    return JsonResponse(json_response)

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
                # Use the view below to create an auth token, then grab it
                create_auth(request)
                auth = (Authenticator.objects.get(user=user))
                json_response = {
                    'status': 'success',
                    'auth': auth.authenticator,
                }
                return JsonResponse(json_response,safe=False)
            else:
                json_response = {
                    'status': 'error',
                    'response':'Incorrect Password',
                }
                return JsonResponse(json_response)
        except ObjectDoesNotExist:
            json_response = {
                'status': 'error',
                'response':'User does not exist',
            }
            return JsonResponse(json_response)
    json_response = {
        'status': 'error',
        'response':'POST request expected. GET request found.',
    }
    return JsonResponse(json_response)


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
            json_response = {
                'status':'success',
                'user':auth.user.username,
                'auth':auth.authenticator,
                'date_created':auth.date_created,
            }
            return JsonResponse(json_response)
        except Exception as e:
            json_response = {
                'status': 'error',
                'response': str(e),
            }
            return JsonResponse(json_response)

    json_response = {
        'status': 'Error: must make POST request'
    }
    return JsonResponse(json_response)

#   Create an method to get all the users
def readAll(request):
    if request.method == 'GET':
        json_response = {
            'status': 'success',
            'response': serializers.serialize("json", myUser.objects.all()),
        }
        return JsonResponse(json_response)

    if request.method == 'POST':
        json_response = {
            'status': 'error',
            'response': 'POST request expected. GET request found.',
        }
        return JsonResponse(json_response)
