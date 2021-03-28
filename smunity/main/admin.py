from django.contrib import admin
from .models import User,Community,Company,Event,Category,Interest

# Register your models here.
admin.site.register(User)
admin.site.register(Community)
admin.site.register(Company)
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Interest)