# Uncomment next two lines to enable admin:
#from django.contrib import admin
#from django.urls import path

from django.urls import path
from . import views
from .views import save_screenshot

urlpatterns = [
    path('video_feed/<int:camera_id>/', views.video_feed, name='video_feed'),
    path('', views.index, name='index'),
    path('save-screenshot/', save_screenshot, name='save_screenshot'),
]
