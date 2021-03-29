from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import User,Community,Company,Event,Interest,Notification
from django.contrib.auth import login, logout,authenticate
from django.views.decorators.csrf import csrf_exempt
from .serializers import EventSerializer,CommunitySerializer,NotificationSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
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

def RegisterInterests(request):
    if request.methods=="POST":
        interests=eval(request.POST.get("interests"))
        user=request.user
        for i in interests:
            interest= Interest.objects.get(name=i)
            user.interest.add(interest)
        user.save()
        return HttpResponse(status=201)

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
@csrf_exempt
def RegisterEvent(request):
    if request.method == "POST":
        title=request.POST.get("title")
        category=request.POST.get("category")
        description=request.POST.get("description")
        organizer_comm=Community.objects.get(members= request.user)
        print(organizer_comm)
        event_date= request.POST.get("date")
        tagline=request.POST.get("tagline")
        mode=request.POST.get("mode")
        link=request.POST.get("link")
        speaker=request.POST.get("speaker")        
        starting_time=request.POST.get("startingtime")
        event=Event.objects.create(
            title=title,
            description=description,
            category=category,
            
            event_date=event_date,
            tagline=tagline,
            mode=mode,
            external_link=link,
            speaker=speaker,
            starting_time=starting_time
        )
        event.organizer.add(organizer_comm)
        event.save()
       
        # notification=Notification.objects.create(
        # created_by=event.organizer.all()[0],
        # event=event,
        # text=f"{event.organizer.all()[0]} Created {event.title}"
        # )
        return HttpResponse(status=201)

@csrf_exempt
def Search(request):
    if request.method=="POST":
        Filter=request.POST.get("filter")
        search=request.POST.get("search")
        search_keywords=search.split(" ")
        # communities=Community.objects.filter(name___in=search_keywords)        
        communities=[]
        
        for word in search_keywords:
            if Filter =="":
                communities_search=Community.objects.filter(name__contains=word)
            else:
                communities_search=Community.objects.filter(Q(city__contains=Filter) & Q(name__contains=word))
            for community in communities_search:
                communities.append(community)
        communities_data=CommunitySerializer(communities,many=True).data
        return JsonResponse({"communities":communities_data},status=201)


class EventList(generics.ListCreateAPIView): # for just GET POST request
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class CommunityList(generics.ListCreateAPIView): # for just GET POST request
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

class CommunityDetails(generics.RetrieveUpdateDestroyAPIView): # for just GET POST request
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

class NotificationList(generics.ListCreateAPIView): # for just GET POST request
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

