from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Sensor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, help_text="Enter Device's Location")

    is_overriden = models.BooleanField(default=False)
    is_warning = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'

# Create your models here.
class SensorReading(models.Model):
    device_id = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    tds = models.FloatField(help_text="Sensor Reading for TDS")
    temp = models.FloatField(help_text="Sensor Reading for temperature")
    pH = models.FloatField(help_text="Sensor Reading for pH Level")

    is_safe_tds = models.BooleanField(default=False, help_text="True if TDS is within standards")
    is_safe_temp = models.BooleanField(default=False, help_text="True if temperature is within standards")
    is_safe_pH = models.BooleanField(default=False, help_text="True if pH is within standards")

    class Meta:
        ordering = ['device_id', '-timestamp']

    def __str__(self):
        return f'{self.device_id} - ({self.timestamp})'

class ServerData(models.Model):
    response_id = models.CharField(primary_key=True, max_length=20, help_text="Enter Response's ID")
    expert_id = models.CharField(max_length=20, help_text="Enter Expert's ID")
    destination_device = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    is_unsafe = models.BooleanField(default=False, help_text="True if the water is contaminated")
    valve_shutoff = models.BooleanField(default=False, help_text="True if the water is contaminated")

    class Meta:
        ordering = ['response_id', 'destination_device', 'is_unsafe']

    def __str__(self):
        return f'{self.response_id} Contamination: {self.is_unsafe}'
