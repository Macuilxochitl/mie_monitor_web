from django.urls import path



from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('get_latest_img/', views.get_latest_img, name='get_latest_img'),
]
