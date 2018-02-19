from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from .forms import SignUpUser, SignUpStudent
from .models import Student

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
    # Format the JSON Response for a GET Request
    if request.method == 'GET':
        # Imported from django
        # Gives you model, pk, fields - user, year
        data = serializers.serialize("json", Student.objects.filter(id=pk))

    # Format the JSON Response for a POST Request
    elif request.method == 'POST':
        # TO DO
        response = JsonResponse({'foo': 'buzz'})
    return HttpResponse(data, content_type='application/json')
