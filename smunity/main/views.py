from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import User,Community,Company
from django.contrib.auth import login, logout,authenticate
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def signup(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        first_name=request.POST.get("firstname")
        last_name=request.POST.get("lastname")
        dob=request.POST.get("dob")
        city= request.POST.get("city")
        password=request.POST.get("password")
        profile_picture=request.FILES.get("profile_picture")
        user=User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            dob=dob,
            city=city,
            
        )
        if profile_picture!= None:
            user.profile_picture=profile_picture
        user.set_password(password)
        user.save()
        return HttpResponse(status=200)
@csrf_exempt
def Login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return JsonResponse ({"user":username},status=200)
        else:
            return HttpResponse(status=400)
@csrf_exempt
def RegisterCommunity(request):
    if request.method== "POST":
        name=request.POST.get("name")
        description=request.POST.get("description")
        category=request.POST.get("category")
        category=category.objects.get(name=category)
        city=reqeust.POST.get("city")
        country=request.POST.get("country")
        image=request.POST.get("image")
        community=Community.objects.create(
            name=name,
            description=description,
            category=category,
            city=city,
            country=country,
            image=image
        )
        community.memmbers.add(request.user)
        community.save()
        return HttpResponse(status=200)
def RegisterCompany(request):
    if request.method=="POST":
        name=request.POST.get("name")
        description=request.POST.get("description")
        link=request.POST.get("link")
        image=request.FILES.get("image")
        company=Company.objects.get(
            name=name,
            description=description,
            link=link,
            image=image
        )
        return HttpResponse(status=200)
    return JsonResponse({"message":"Get request not supported"},status=400)

