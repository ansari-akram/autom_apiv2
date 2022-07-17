from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
import uuid


class HAUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField()
    change_request = models.BooleanField(default=False)
    change_uuid = models.CharField(max_length=100, default="", editable=False)

    def __str__(self) -> str:
        return self.user.__str__()


class Room(models.Model):
    user = models.ForeignKey(HAUser, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.room_name


class MCU4(models.Model):
    user = models.ForeignKey(HAUser, on_delete=models.CASCADE)
    btn1 = models.BooleanField(default=False)
    btn2 = models.BooleanField(default=False)
    btn3 = models.BooleanField(default=False)
    btn4 = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.user.username.__str__()


class MCUType(models.Model):
    mcu_type = models.IntegerField()

    def __str__(self) -> str:
        return self.mcu_type.__str__()


class MCU8(models.Model):
    user = models.ForeignKey(HAUser, on_delete=models.CASCADE)
    mcu_name = models.CharField(default='', max_length=100)
    mcu_type = models.ForeignKey(MCUType, on_delete=models.CASCADE)
    mcu_ip = models.GenericIPAddressField(default="0.0.0.0")

    def __str__(self) -> str:
        return self.user.user.username.__str__() + "-" + self.mcu_name.__str__() + "-" + self.mcu_type.__str__()


class RoomDevice(models.Model):
    user = models.ForeignKey(HAUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    mcu = models.ForeignKey(MCU8, on_delete=models.CASCADE)
    btn_no = models.IntegerField()
    btn_state = models.BooleanField(default=False)
    device_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.device_name