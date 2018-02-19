from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse

from students.models import Student

from . import forms

def index(request):
    return render(request, 'index.html')

def loginUser(request):
    if request.user.is_authenticated():
        return render(request, 'login.html', {'message': 'You are already logged in as {}'.format(request.user.username)})

    form = forms.LogInUser()
    if request.method == 'POST':
        loginForm = forms.LogInUser(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #redirect to the correct profile based on the user type
                if Student.objects.filter(user=user.id).exists():
                    return HttpResponseRedirect(reverse('students:profile',))
                else:
                    return HttpResponseRedirect(reverse('index',))

            else:
                return render(request, 'login.html', {'message':'Username or password incorrect', 'form':form})

        return render(request, 'login.html', {'message':loginForm.errors})

    return render(request, 'login.html', {'form':form})
