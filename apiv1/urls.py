from venv import create
from .views import *
from django.conf.urls import url
from rest_framework import routers
from django.urls import path, include


router = routers.DefaultRouter()
# router.register('user', UserViewSet)
router.register('room', RoomViewSet)
router.register('mcu', MCU8ViewSet)
router.register('room_device', RoomDeviceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('forget-password/', forget_password, name='forget_password'),
    path('set-password/', set_password, name='set_password'),
]