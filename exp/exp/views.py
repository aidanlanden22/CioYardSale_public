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
        encode_data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/users/create_user/', data=encode_data, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
       # resp = json.loads(resp_json)
        #if resp['response'] == 'username taken':
        #    return JsonResponse({'response':'username taken'})
        #user = resp['response']
        #auth_post_data = {'username':request.POST.get('username'), 'password':request.POST.get('password')}
        #auth_post_encoded = urllib.parse.urlencode(auth_post_data).encode('utf-8')
        #auth_req = urllib.request.Request('http://models-api:8000/api/v1/user/login/', data=auth_post_encoded, method='POST')
        #resp_json = urllib.request.urlopen(auth_req).read().decode('utf-8')
        print("hey")
        #auth_resp = json.loads(resp_json)
        return JsonResponse(resp, safe=False)
        #return JsonResponse({'user':resp,'response': 'success'})
        #check if user already exists

        #login user
    #return JsonResponse(resp, safe=False)
