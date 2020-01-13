from django.contrib import admin

from .models import House, Room, Control, ControlState, SensorState, Sensor

# Register your models here.

admin.site.register(House)
admin.site.register(Room)
admin.site.register(Control)
admin.site.register(Sensor)
admin.site.register(ControlState)
admin.site.register(SensorState)
