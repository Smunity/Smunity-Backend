from django.test import TestCase
from .models import User,Community,Category,Event
from .serializers import EventSerializer
# Create your tests here.
class InitialTest(TestCase):
    def Setup(self):
        self.user=User.objects.create_user("Syed Bilal","Ali","syed.bilal.sba@gmail.com",'syedbilal28','hellojee')
    def test1(self):
        user=User.objects.create_user("Syed Bilal","syed.bilal.sba@gmail.com",'syedbilal28')
        category=Category.objects.create(
            name="Programming",
            description="dummy"
        )
        name="DSC"
        description="Dummy Description"
        category="Programming"
        category=Category.objects.get(name=category)
        city="Karachi"
        country="Pakistan"
        # image=request.POST.get("image"
        community=Community.objects.create(
            name=name,
            description=description,
            category=category,
            city=city,
            country=country,
            # image=image
        )
        community.members.add(user)
        community.save()
        title="Event1"
        category="Programming"
        description="A short description of the event"
        organizer=Community.objects.get(members=user.pk)
        print(organizer)
        event_date= "2021-10-12"
        tagline="We are the best"
        mode="physcial"
        link="Just a dummy link"
        speaker="Phunksukh Wangdu"        
        starting_time="12:00 am"
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
        event_data=EventSerializer(event).data
        print(event_data)