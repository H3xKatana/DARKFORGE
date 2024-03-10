# the project is session based to stop CRSF+XSS
# defined endpoints 

from django.shortcuts import render
import json 
from django.contrib.auth import login,logout,authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
# Create your views here.



@require_POST
#djanog predifne to ensure that function is accesd with post only
def login_view(request):
    data=json.loads(request)
    username=data.get("username")
    password=data.get("password")
    #email=data.get("email")
    #Techlvl=data.get("Techlvl")


    if username is None or password is None:
        return JsonResponse({'detail':'username and password must be provided'})
    
    user=authenticate(username=username,password=password)

    if user is None :
        return JsonResponse({'detail':'invalid login info '},status=400)
    login(request,user)
    return JsonResponse({'detail':'Succesfully logged in ! , Welcome {username}'})



def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail':'you are not logged in'},status=400)
    logout(request)
    return JsonResponse({'detail':'Succesfully logged out !'})


@ensure_csrf_cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"is_authenticated":False})
    return JsonResponse({"is_authenticated":True})


def whoami_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"is_authenticated":False})
    return JsonResponse({"user profile":request.user.username})