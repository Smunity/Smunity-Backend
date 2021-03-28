from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns=[
    path('signup/',views.signup,name="signup"),
    path('login/',views.Login,name="login"),
    path('events/',views.EventList.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)