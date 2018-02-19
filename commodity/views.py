from django.shortcuts import render
from django.http import HttpResponse

def sell(request):
    return render(request, 'commodity/createcommodity.html')