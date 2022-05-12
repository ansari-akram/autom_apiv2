from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class HAUserSerializers(serializers.ModelSerializer):

    class Meta:
        model = HAUser
        fields = ['id', 'user', 'phone']


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'user', 'room_name']


class MCU8Serializer(serializers.ModelSerializer):

    class Meta:
        model = MCU8
        fields = ['id', 'user', 'mcu_type', 'mcu_name']


class RoomDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomDevice
        fields = ['id', 'user', 'room', 'mcu', 'btn_no', 'btn_state', 'device_name']
