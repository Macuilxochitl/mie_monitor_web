from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Image
import time
from django.http import JsonResponse
import requests
import os
import json
from mie_monitor_web.settings import host
from django.core.mail import send_mail
from mie_monitor_web.settings import EMAIL_HOST_USER


body_detect_url = 'https://api-cn.faceplusplus.com/humanbodypp/v1/detect'
face_detect_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'

key = os.environ.get("facepp_key")
secret = os.environ.get("facepp_secret")

latest_img = None
latest_send_email_time = None

enable_alert = True

person_threshold = 2

try:
    latest_img = Image.objects.all().last()
except:
    print("init image error.")


@csrf_exempt
def index(request):
    return HttpResponse("Hello, world.")


@csrf_exempt
def set_alert(request):
    global enable_alert, person_threshold
    print(enable_alert)
    print(person_threshold)
    req = json.loads(request.body.decode("utf-8"))
    print(req)
    enable_alert = req['enable']
    if req['num']:
        try:
            person_threshold = int(req['num'])
        except:
            print('person_threshold must be int.')
    return HttpResponse("ok.")


def get_latest_img(request):
    global latest_img
    if not latest_img:
        return HttpResponse("")
    return JsonResponse({'face_detect_result': latest_img.face_detect_result,
                         'body_detect_result': latest_img.body_detect_result,
                         'img_url': host + latest_img.img.url})


def get_alert_setting(request):
    global enable_alert, person_threshold
    return JsonResponse({'enable_alert': enable_alert,
                         'person_threshold': person_threshold})


def get_latest_face_detect_img(request):
    global latest_img
    if not latest_img:
        return HttpResponse("")
    faces_set = latest_img.get_face_set()
    return JsonResponse({'face_detect_result': latest_img.face_detect_result,
                         'body_detect_result': latest_img.body_detect_result,
                         'img_url': host + latest_img.img.url,
                         'faces': faces_set})


def get_latest_body_detect_img(request):
    global latest_img
    if not latest_img:
        return HttpResponse("")
    latest_img.rect_body()
    return JsonResponse({'face_detect_result': latest_img.face_detect_result,
                         'body_detect_result': latest_img.body_detect_result,
                         'img_url': host + latest_img.rect_body_img.url})


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
                           data={'api_key': key, 'api_secret': secret, 'return_attributes': 'gender,age,emotion'},
                           files={'image_file': img})

    image.body_detect_result = json.loads(r_body.text)["humanbodies"]
    image.face_detect_result = json.loads(r_face.text)["faces"]
    global latest_img
    latest_img = image
    image.save()
    if len(image.body_detect_result) >= person_threshold:
        alert()
    return JsonResponse({'msg': 'upload done.'})


def alert():
    global latest_send_email_time, person_threshold, enable_alert
    if not latest_send_email_time or time.time() - latest_send_email_time > 60 and enable_alert:
        print("send email.")
        send_mail('智能监控系统 ———— 报警', '智能监控系统侦测到有{0}人以上出现，请注意.'.format(person_threshold), EMAIL_HOST_USER, ['admin@yitu.yt', '307535705@qq.com', '852917283@qq.com'], fail_silently=False)
        latest_send_email_time = time.time()


def statistics(request):
    img = Image.objects.all()
    count = 0
    max_num = 0
    for i in img:
        try:
            num = len(eval(i.body_detect_result))
        except Exception as e:
            continue
        count += num
        if num > max_num:
            max_num = num
    avg = count / len(img)
    return JsonResponse({'mon_data': {'avg': round(avg, 2), 'count': count, 'max': max_num}})
