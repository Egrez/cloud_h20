from django.shortcuts import render, HttpResponse
from sensors.models import Sensor, SensorReading, ServerData

import json

import datetime

# Create your views here.
def home(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        sensor_readings = SensorReading.objects.all()[0:15]

        obj = {}
        for index in range(len(sensor_readings)):
            reading = sensor_readings[index]

            timestamp = reading.timestamp.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)

            obj[index] = [reading.device_id.user.username, str(reading.pH), str(reading.tds), str(reading.temp), reading.is_safe_pH, reading.is_safe_tds, reading.is_safe_temp, datetime.datetime.strftime(timestamp, "%B %d, %Y, %#I:%M %p")]

        return HttpResponse(json.dumps(obj, default=str))
    else:
        sensors = Sensor.objects.all()
        sensor_readings = SensorReading.objects.all()[0:15]
        server_data = ServerData.objects.all()
        locations = Sensor.objects.values_list('location', flat=True).distinct()

        return render(request, "index.html", { 'sensors': sensors, 'sensor_readings': sensor_readings, 
                                            'server_data': server_data, 'locations': locations })