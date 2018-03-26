from django.shortcuts import render
from django.contrib.auth import hashers
from django.views.decorators.csrf import csrf_exempt

from .models import myUser, Authenticater

# From the Project 4 documentation
import os
import hmac
from CioYardSale import settings

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
            user = customer.objects.get(username=request.POST.get('username'))
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
                'status': str(e)
            }
            return JsonResponse(json_response)

    json_response = {
        'status': 'Error: must make POST request'
    }
    return JsonResponse(json_response)
