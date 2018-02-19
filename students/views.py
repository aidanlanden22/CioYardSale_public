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

def profile(request):
    myKey = request.user.id
    return render(request, 'students/profile.html', {'myKey': myKey })

def signup(request):
    if request.user.is_authenticated and Student.objects.filter(user=request.user).exists():
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        userForm = SignUpUser(request.POST)
        studentForm = SignUpStudent(request.POST)
        formErrors = {}
        formErrors.update(userForm.errors)
        formErrors.update(studentForm.errors)
        if userForm.is_valid() and studentForm.is_valid():
            user = User.objects.create_user(
                username=userForm.cleaned_data['username'],
                password=userForm.cleaned_data['password'],
                first_name=userForm.cleaned_data['first_name'],
                last_name=userForm.cleaned_data['last_name'],
                email=userForm.cleaned_data['email']
            )
            user.save()
            student = studentForm.save(commit=False)
            student.user = user
            student.save()
            login(request, user)
            return HttpResponseRedirect(reverse('students:profile'))

        return render(request, 'students/signup.html', {'errors': formErrors,  'userForm': userForm, 'studentForm': studentForm})

    userForm = SignUpUser()
    studentForm = SignUpStudent()
    return render(request, 'students/signup.html', {'userForm': userForm, 'studentForm': studentForm})

def logoutUser(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect(reverse('index'))


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
            user = User.objects.create_user(
                username = request.POST.get('username'),
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
                email = request.POST.get('email'),
                password = hashers.make_password(request.POST.get('password'))
            )
            user.save()

            student = Student.objects.create(
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
        # TO DO
        data = {}
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
