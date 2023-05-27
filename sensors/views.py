from django.shortcuts import render
from sensors.models import Sensor, SensorReading, ServerData

import requests

from django.contrib.auth import authenticate, login

# Create your views here.
def home(request):
	return render(request, "index.html")

def signin(request):
	username = request.POST["username"]
	password = request.POST["password"]
	user = authenticate(request, username=username, password=password)

	if user is not None:
		login(request, user)

	return render(request, "index.html")

def sensor(request): # POST Request for Sensor Readings
	if request.user.is_authenticated:
		user = request.user
		device_id = user.sensor
		
		data = request.POST['data']

		#Timestamp should be automatically assigned when saved
		new_obj = SensorReading(device_id=device_id, data=data)
		new_obj.save()

	# Render the HTML template with the data in the context variable
	return render(request, "index.html")

def send_warning_signal(request): # POST Request to turn on LEDs
	post_data = {'name': 'Gladys'}

	# replace this with IP address and port number of client sensors
	response = requests.post('http://example.com', data=post_data)
	content = response.content

	print(content)
	# Render the HTML template with the data in the context variable
	return render(request, "index.html")