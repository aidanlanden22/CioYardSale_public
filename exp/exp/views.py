import urllib.request
import urllib.parse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
            #'year':request.POST.get('year'),
        }

        #if // 'Username already exists.'


        encode_data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/users/create_user/', data=encode_data, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)

        #if resp['response'] == 'Username already exists.':
        #    return resp

        #login user
    return JsonResponse(resp, safe=False)

def loginUser(request):
    if request.method == 'POST':
        post_data = {'username': request.POST.get('username'),
                     'password':request.POST.get('password')}
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/user/login/', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return JsonResponse({'resp':resp})

@csrf_exempt
def logoutUser(request):
    if request.method == 'POST':
        data = {'auth': request.POST.get('auth')}
        data_encoded = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/auth/delete/', data=data_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return JsonResponse(resp, safe=False)
