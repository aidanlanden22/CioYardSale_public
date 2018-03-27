from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from .forms import SignUpUser, SignUpStudent
from .models import Student

# API
from django.contrib.auth import hashers
from django.http import JsonResponse
from django.core import serializers
import json

# ********** THIS IS THE API FOR STUDENTS **********
def read(request, pk):
    data = {}
    if request.method == 'GET':
        data = serializers.serialize("json", User.objects.filter(id=pk), fields=('username', 'first_name', 'last_name', 'email', 'date_joined'))
    elif request.method == 'POST':
        status = {'status': 'unsucessful request'}
        data = json.dumps(status)
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
                #first_name = request.POST.get('first_name'),
                #last_name = request.POST.get('last_name'),
                #email = request.POST.get('email'),
                password = hashers.make_password(request.POST.get('password'))
            )
            myUser.save()

            student = Student.objects.create(
                user = myUser,
                user_id = myUser.id,
                year = request.POST.get('year'),
            )
            student.save()
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
        if request.POST.get('first_name'):
            user.first_name = request.POST.get('first_name')
            user.save()
            status = {'status': 'sucessful request', 'action': 'updated firstname'}
        if request.POST.get('last_name'):
            user.last_name = request.POST.get('last_name')
            user.save()
            status = {'status': 'sucessful request', 'action': 'updated lastname'}
        if request.POST.get('email'):
            user.email = request.POST.get('email')
            user.save()
            status = {'status': 'sucessful request', 'action': 'updated email'}
        if request.POST.get('year'):
            user.year = request.POST.get('year')
            user.save()
            status = {'status': 'sucessful request', 'action': 'updated year'}
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
