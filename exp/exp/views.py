import urllib.request
import urllib.parse
import json
from django.http import JsonResponse

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

def registerStudent(request):
    if request.method == 'POST':
        data = {
            'username': request.POST.get('username'),
            'password':request.POST.get('password'),
            'year':request.POST.get('year'),
        }
        req = urllib.request.Request('http://models-api:8000/api/v1/student/create/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)

        #check if user already exists

        #login user
    return JsonResponse(resp, safe=False)
