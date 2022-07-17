from django.contrib import admin
from .models import *


class HAUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'change_request', 'change_uuid')


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_name')


class MCU8Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'mcu_name', 'mcu_type', 'mcu_ip')


class RoomDeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'mcu', 'btn_no', 'btn_state', 'device_name')


admin.site.register(HAUser, HAUserAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(MCU8, MCU8Admin)
admin.site.register(RoomDevice, RoomDeviceAdmin)
admin.site.register(MCUType)

# root admin