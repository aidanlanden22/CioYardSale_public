from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from .forms import SignUpUser, SignUpStudent
from .models import Student


def profile(request):
    return render(request, 'students/profile.html')

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
    return render(request, 'index.html')
