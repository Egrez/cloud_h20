from django.shortcuts import render
from sensors.models import Sensor, SensorReading, ServerData

import requests

from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.http import HttpResponse

@csrf_exempt
def signin(request):
	username = request.POST["username"]
	password = request.POST["password"]

	user = authenticate(request, username=username, password=password)

	if user is not None:
		login(request, user)

	return render(request, "index.html")

# user controlled input to turn on LEDs
def send_warning_signal(request, id): 
	channel_layer = get_channel_layer()
	async_to_sync(channel_layer.group_send)(
		'QC',
		{
			'type': 'send_warning',
			'message': 'Test message'
		}
	)
	return HttpResponse('<p>Warning signal sent</p>')