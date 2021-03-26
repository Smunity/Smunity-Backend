from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from django.contrib.auth import login, logout,authenticate
# Create your views here.

def Signup(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        first_name=request.POST.get("firstname")
        last_name=request.POST.get("lastname")
        dob=request.POST.get("dob")
        city= request.POST.get("city")
        profile_picture=request.FILES.get("profile_picture")
        user=User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            dob=dob,
            city=city,
            profile_picture=profile_picture
        )
        user.set_password(password)
        user.save()
        return JsonResponse(status=200)

def login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return JsonResponse ({"user":username},status=200)
        else:
            return JsonResponse(status=400)
    
        