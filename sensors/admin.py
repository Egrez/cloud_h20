from django.contrib import admin
from .models import Sensors, ServerData

# Register your models here.
admin.site.register(Sensors)
admin.site.register(ServerData)