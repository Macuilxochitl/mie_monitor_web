from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('get_latest_img/', views.get_latest_img, name='get_latest_img'),
    path('get_latest_body_detect_img/', views.get_latest_body_detect_img, name='get_latest_body_detect_img'),
    path('get_latest_face_detect_img/', views.get_latest_face_detect_img, name='get_latest_face_detect_img'),
    path('set_alert/', views.set_alert, name='set_alert'),
]
