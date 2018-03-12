# VIEWS IN THE EXPERIENCE LAYER SHOULD JUST PASS ON JSON INFO
# EXAMPLE: DISPLAY TOP 10 ITEMS ON HOME PAGE

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse


# SIGNUP FOR CIO --- SHOULD JUST CALL CREATE
def CIOsignup(request):
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

# LOGOUT FOR GENERAL USER
def logoutUser(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect(reverse('index'))

# CREATE A NEW ITEM TO SELL
# def sell(request):
#     return render(request, 'createcommodity.html')
