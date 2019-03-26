from django.contrib import admin
from .models import Image
from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.site_header = 'Monitor administration'

# Register your models here.

admin.site.register(Image)
admin.site.unregister(Group)
