from django.db import models

# Create your models here.
class Sensors(models.Model):
    device_id = models.CharField(primary_key=True, max_length=20, help_text="Enter Device's Name")
    timestamp = models.DateTimeField(primary_key=True, auto_now=True)
    location = models.CharField(max_length=50, help_text="Enter Device's Location")
    data = models.FloatField(help_text="Sensor Reading")

    class Meta:
        ordering = ['device_id', '-timestamp']

    def __str__(self):
        return f'{self.device_id} in {self.location} ({self.timestamp})'

class ServerData(models.Model):
    response_id = models.CharField(primary_key=True, max_length=20, help_text="Enter Response's ID")
    expert_id = models.CharField(max_length=20, help_text="Enter Expert's ID")
    destination_device = models.CharField(max_length=20, help_text="Enter Destination Device's Name")
    is_unsafe = models.BooleanField(default=False, help_text="True if the water is contaminated")
    valve_shutoff = models.BooleanField(default=False, help_text="True if the water is contaminated")

    class Meta:
        ordering = ['response_id', 'destination_device', 'is_unsafe']

    def __str__(self):
        return f'{self.response_id} Contamination: {self.is_unsafe}'
