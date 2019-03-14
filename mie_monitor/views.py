from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Image
import time
from django.core.files.base import ContentFile


@csrf_exempt
def index(request):
    print(request.FILES)
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def upload(request):
    image = Image(file_path=request.FILES['image'])
    print(image)
    image.save()
    time.sleep(5)
    return HttpResponse(1)
