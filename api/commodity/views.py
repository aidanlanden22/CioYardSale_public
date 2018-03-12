from django.shortcuts import render
from .forms import CommodityForm, CommodityPicForm
from .models import Commodity
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt


from django.core import serializers
import json

# ********** THIS IS THE API FOR COMMODITIES **********
@csrf_exempt
def read(request, pk):
    # Format the JSON Response for a GET Request
    if request.method == 'GET':
        # Imported from django
        # Gives you model, pk, fields - user, year

        data = serializers.serialize("json", Commodity.objects.filter(id=pk))
        return HttpResponse(data, content_type='application/json')

    if request.method == 'POST':
        status = {'status': 'unsucessful request'}
        data = json.dumps(status)
        return HttpResponse(data, content_type='application/json')


@csrf_exempt
def create(request):

    if request.method == 'POST':
        form = CommodityForm(request.POST)

        if form.is_valid():

            selling = Commodity.objects.create(
                g_or_s=form.cleaned_data['g_or_s'],
                quantity=form.cleaned_data['quantity'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                date_expires=form.cleaned_data['date_expires'],
                title=form.cleaned_data['title'],
                cio=request.user
            )

            selling.save()

            data = serializers.serialize("json", [selling])
            return HttpResponse(data, content_type='application/json')

    if request.method == 'GET':
        status = {'status': 'unsucessful request'}
        data = json.dumps(status)
        return HttpResponse(data, content_type='application/json')

@csrf_exempt
def update(request, pk):
    data = {}
    if request.method == 'GET':
        status = {'status': 'unsucessful request'}
        data = json.dumps(status)
    elif request.method == 'POST':
        try:
            commodity = Commodity.objects.get(id=pk)
        except Exception as e:
            return JsonResponse({'status': str(e)})
        status = {'status': 'unsucessful request', 'action': 'nothing updated'}
        if request.POST.get('g_or_s'):
            commodity.username = request.POST.get('g_or_s')
            commodity.save()
            status = {'status': 'sucessful request', 'action': 'updated good or service'}
        if request.POST.get('title'):
            commodity.title = request.POST.get('title')
            commodity.save()
            status = {'status': 'sucessful request', 'action': 'updated title'}
        if request.POST.get('description'):
            commodity.last_name = request.POST.get('description')
            commodity.save()
            status = {'status': 'sucessful request', 'action': 'updated description'}
        if request.POST.get('quantity'):
            commodity.email = request.POST.get('quantity')
            commodity.save()
            status = {'status': 'sucessful request', 'action': 'updated quantity'}
        if request.POST.get('price'):
            commodity.year = request.POST.get('price')
            commodity.save()
            status = {'status': 'sucessful request', 'action': 'updated price'}
        if request.POST.get('date_expires'):
            commodity.year = request.POST.get('date_expires')
            commodity.save()
            status = {'status': 'sucessful request', 'action': 'updated date expired'}
        response = {'g_or_s': commodity.g_or_s,'title': commodity.title,
                'description': commodity.description, 'quantity': commodity.quantity, 'price': commodity.price, 'date_expires': commodity.date_expires}
        full_response = {'status': status, 'response': response}
        data = json.dumps(full_response)

    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def delete(request, pk):
    data = {}
    if request.method == 'GET':
        status = {'status': 'unsucessful request'}
        data = json.dumps(status)
    elif request.method == 'POST':
        commodity = Commodity.objects.filter(id=pk)
        commodity.delete()
        status = {'status': 'sucessful request', 'action': 'deleted commodity'}
        data = json.dumps(status)

    return HttpResponse(data, content_type='application/json')
