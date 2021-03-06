from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Commodity, Recommendation

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
def readAll(request):
    # Format the JSON Response for a GET Request
    if request.method == 'GET':
        data = serializers.serialize("json", Commodity.objects.all())
        return HttpResponse(data, content_type='application/json')

    if request.method == 'POST':
        status = {'status': 'unsucessful request'}
        data = json.dumps(status)
        return HttpResponse(data, content_type='application/json')

@csrf_exempt
def create(request):
    json_response = {}
    if request.method == 'POST':
        try:
            selling = Commodity.objects.create(
                g_or_s=request.POST.get('g_or_s'),
                quantity=request.POST.get('quantity'),
                description=request.POST.get('description'),
                price=request.POST.get('price'),
                date_expires=request.POST.get('date_expires'),
                title=request.POST.get('title'),
            )
            selling.save()
            #data = serializers.serialize("json", Commodity.objects.filter(id=selling.pk))
            data = selling.pk
            #data = serializers.serialize("json", [selling])
            json_response = {
                'status': 'success',
                'response': data,
            }
            return JsonResponse(json_response)

        except Exception as e:
            json_response = {
                'status': 'error',
                'response': str(e),
            }
            return JsonResponse(json_response)

    if request.method == 'GET':
        json_response = {
            'status': 'error',
            'response': 'POST request expected. GET request found.',
        }
        data = json.dumps(json_response)
        return JsonResponse(json_response)
    return JsonResponse(json_response)

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

@csrf_exempt
def getRecs(request, pk):
    data = {}
    if request.method == 'POST':
        status = {'status': 'unsucessful request'}
        data = json.dumps(status)
    elif request.method == 'GET':
        data = serializers.serialize("json", Recommendation.objects.filter(item_id=pk))
        return HttpResponse(data, content_type='application/json')