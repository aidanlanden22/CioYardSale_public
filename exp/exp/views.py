import urllib.request
import urllib.parse
import json
from django.http import JsonResponse

def getCommodityList(request):
    req = req = urllib.request.Request('http://models-api:8000/api/v1/commodity/readAll/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    return JsonResponse(resp, safe=False)

def getSingleCommodity(request,pk):
    req = req = urllib.request.Request('http://models-api:8000/api/v1/commodity/' + pk + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    return JsonResponse(resp, safe=False)
