from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Image
import time
from django.http import JsonResponse
import requests
import os


body_detect_url = 'https://api-cn.faceplusplus.com/humanbodypp/v1/detect'
face_detect_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'

key = os.environ.get("key")
secret = os.environ.get("secret")


latest_img = None


@csrf_exempt
def index(request):
    return HttpResponse("Hello, world.")


def get_latest_img(request):
    global latest_img
    if not latest_img:
        return HttpResponse("")
    return JsonResponse({'face_detect_result': latest_img.face_detect_result,
                         'body_detect_result': latest_img.body_detect_result,
                         'img_url': latest_img.img.url})


@csrf_exempt
def upload(request):
    image = Image(img=request.FILES['image'])
    image.save()
    img = open(image.img.path, 'rb')

    r_body = requests.post(body_detect_url,
                           data={'api_key': key, 'api_secret': secret, 'return_attributes': 'gender'},
                           files={'image_file': img})

    img = open(image.img.path, 'rb')

    r_face = requests.post(face_detect_url,
                           data={'api_key': key, 'api_secret': secret, 'return_attributes': 'gender'},
                           files={'image_file': img})

    image.body_detect_result = r_body.text
    image.face_detect_result = r_face.text
    global latest_img
    latest_img = image
    image.save()
    return JsonResponse({'msg': 'upload done.'})
