from django.contrib import admin
from .models import Image

admin.site.site_header = 'Monitor administration'

# Register your models here.

admin.site.register(Image)
