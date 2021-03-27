from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.conf import settings
from django_countries.fields import CountryField
# Create your models here.



def upload_user_image(instance,filename):
    # path_to_upload=os.path(instance.username+"/ProfilePicture")
    directory= os.path.join(settings.MEDIA_ROOT,instance.username)
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    directory_profile = os.path.join(directory,'ProfilePicture')
    try:
        os.stat(directory_profile)
    except:
        os.mkdir(directory_profile)
    return f"{instance.username}/ProfilePicture/{filename}"

def upload_smunity_image(instance,filename):
    directory= os.path.join(settings.MEDIA_ROOT,instance.name)
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    return f"{instance.name}/{filename}"

class User(AbstractUser):
    dob=models.DateField(max_length=8,null=True)
    city= models.CharField(max_length=50)
    profile_picture=models.ImageField(upload_to=upload_user_image)
    interest=models.ManyToManyField("Interest")
class Interest(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=500)
    image=models.ImageField(upload_to='interests/')

class Category(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=500)

class Community(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    members= models.ManyToManyField(User)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    city=models.CharField(max_length=50,null=True)
    country= CountryField()
    image=models.ImageField(upload_to=upload_smunity_image)

class Event(models.Model):
    title=models.CharField(max_length=100)
    agenda=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    organizer=models.ManyToManyField(Community)
    date_created=models.DateTimeField(auto_now=True)
    event_date=models.DateField()
    tagline=models.CharField(max_length=200)
    #collaborator=models.ManyToManyField(Community)
    #sponsor=models.ManyToManyField("Company")
    MODE_CHOICES=[
        ('phy',"Physical"),
        ('on',"Online")
    ]
    mode=models.CharField(choices=MODE_CHOICES,max_length=3)
    external_link=models.CharField(max_length=100)

class Session(models.Model):
    name=models.CharField(max_length=100)
    starting_datetime=models.DateTimeField()
    speaker=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    topic=models.CharField(max_length=100)
    #time alloted in mins
    timealloted=models.IntegerField()
