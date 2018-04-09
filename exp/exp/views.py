import urllib.request
import urllib.parse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Project 5
from kafka import KafkaProducer
from elasticsearch import Elasticsearch

producer = KafkaProducer(bootstrap_servers='kafka:9092')
es = Elasticsearch(['es'])

from django.shortcuts import render

def search(request):
    # Need to access the elastic search
    global es

    # store all of the items we get back
    items = []

    # WEB layer should be sending a GET request to EXP layer
    if request.method == 'GET':

        # Grab the query from the GET request
        query = request.GET.get('query', '')

        try:
            # call es.search() to query the listing_index for documents that match the query (from Pinckney documentation)
            resp = es.search(index='listing_index', body={'query': {'query_string': {'query': query}}, 'size': 10})

            # Example resp
            # {'timed_out': False, 'hits': {'total': 1, 'hits': [{'_score': 0.10848885, '_index': 'listing_index', '_source': {'id': 42, 'description': 'This is a used Macbook Air in great condition', 'title': 'Used MacbookAir 13"'}, '_id': '42', '_type': 'listing'}], 'max_score': 0.10848885}, '_shards': {'successful': 5, 'total': 5, 'failed': 0}, 'took': 21}
            for resp in resp['hits']['hits']:
                items.append(resp['_source'])

            json_response = {
                'status': 'success',
                'response': "Found items",
                'items': items,
                'error': None
            }
            return JsonResponse(json_response, safe=False)
        except Exception as e:
            json_response = {
                'status': 'error',
                'response': "Could not find items",
                'items': items,
                'error': str(e),
            }
            return JsonResponse(json_response, safe=False)
    else:
        json_response = {
            'status': 'error',
            'response': 'Expected a GET request. Recieved a POST request.',
            'items': items,
            'error': str(e),
        }
        return JsonResponse(json_response, safe=False)

def getCommodityList(request):
    req = urllib.request.Request('http://models-api:8000/api/v1/commodity/readAll/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    return JsonResponse(resp, safe=False)

def getSingleCommodity(request,pk):
    req = urllib.request.Request('http://models-api:8000/api/v1/commodity/' + pk + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    return JsonResponse(resp, safe=False)

@csrf_exempt
def signupUser(request):
    if request.method == 'POST':
        data = {
            'username': request.POST.get('username'),
            'password':request.POST.get('password'),
        }
        encode_data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/users/create_user/', data=encode_data, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)

        return JsonResponse(resp, safe=False)

@csrf_exempt
def createCommodity(request):
    if request.method == 'POST':
        data = {
            'g_or_s': request.POST.get('g_or_s'),
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'price': request.POST.get('price'),
            'quantity': request.POST.get('quantity'),
            'date_expires': request.POST.get('date_expires')
        }
        encode_data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/commodity/create/', data=encode_data, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)

        # Straight from Pinckney documentation
        producer.send('new-listings-topic', json.dumps(item).encode('utf-8'))

        return JsonResponse(resp, safe=False)

def loginUser(request):
    if request.method == 'POST':
        post_data = {'username': request.POST.get('username'),
                     'password':request.POST.get('password')}
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/users/login/', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return JsonResponse({'resp':resp})

@csrf_exempt
def logoutUser(request):
    if request.method == 'POST':
        data = {'auth': request.POST.get('auth')}
        data_encoded = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/users/delete_auth/', data=data_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return JsonResponse({'resp':resp})
