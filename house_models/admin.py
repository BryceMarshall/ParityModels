from django.contrib import admin

from .models import House, Room, Control
# Register your models here.

admin.site.register(House)
admin.site.register(Room)
admin.site.register(Control)

