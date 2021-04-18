from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.conf import settings
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    profile_picture=models.ImageField(upload_to=upload_user_image,null=True,blank=True,default="defaultprofile.jpg")
    interest=models.ManyToManyField("Interest",null=True)
class Interest(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=500)
    def __str__(self):
        return self.name
# class CommunityManager(models.Manager):
#     # def by_user(self,user):
#     def by_user(self, user):
#         qlookup = Q(user1=user) | Q(user2=user)
#         qlookup2 = Q(user1=user) & Q(user2=user)
#         qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
#         return qs

class Community(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    members= models.ManyToManyField(User)
    category=models.ForeignKey("Category",on_delete=models.CASCADE)
    city=models.CharField(max_length=50,null=True)
    country= CountryField()
    image=models.ImageField(upload_to=upload_smunity_image,null=True,blank=True)
    # objects=CommunityManager
    def __str__(self):
        return self.name

class Event(models.Model):
    title=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    organizer=models.ManyToManyField(Community)
    date_created=models.DateTimeField(auto_now=True)
    event_date=models.DateField()
    tagline=models.CharField(max_length=200,null=True,blank=True)
    
    # collaborator=models.ManyToManyField(Community)
    # sponsor=models.ManyToManyField("Company")
    MODE_CHOICES=[
        ('phy',"Physical"),
        ('on',"Online")
    ]
    mode=models.CharField(choices=MODE_CHOICES,max_length=3)
    external_link=models.CharField(max_length=100)
    # speaker=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL)
    speaker=models.CharField(max_length=500,null=True)
    starting_time=models.TimeField(default=None)
    def __str__(self):
        return self.title

@receiver(post_save,sender=Event)
def event_handler(sender,instance,created,*args,**kwargs):
    if len(instance.organizer.all()) >0:    
        notification=Notification.objects.create(
            created_by=instance.organizer.all()[0],
            event=instance,
            text=f"{instance.organizer.all()[0]} Created {instance.title}"
        )    
class Company(models.Model):
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=500)
    link=models.CharField(max_length=200,null=True,blank=True)
    image=models.ImageField(upload_to=upload_smunity_image,null=True,blank=True)

class Notification(models.Model):
    created_by=models.ForeignKey(Community,on_delete=models.CASCADE)
    event= models.ForeignKey(Event,on_delete=models.CASCADE)
    text=models.CharField(max_length=500)
    
    def __str__(self):
        return self.text