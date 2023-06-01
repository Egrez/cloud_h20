from django.shortcuts import render
from sensors.models import Sensor, SensorReading, ServerData

import requests

from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signin(request):
	username = request.POST["username"]
	password = request.POST["password"]
	port = request.POST["port"]
	user = authenticate(request, username=username, password=password)

	sensor = user.sensor
	ip_addr = request.META.get('HTTP_X_FORWARDED_FOR')
	
	sensor.ip_addr = ip_addr
	sensor.port = port
	sensor.save()

	if user is not None:
		login(request, user)

	return render(request, "index.html")

@csrf_exempt
def sensor(request): # POST Request for Sensor Readings
	if request.user.is_authenticated:
		user = request.user
		device_id = user.sensor
		
		print(request.POST)

		tds = request.POST['tds']
		pH = request.POST['pH']
		cond = request.POST['cond']

		#Timestamp should be automatically assigned when saved
		new_obj = SensorReading(device_id=device_id, tds=tds, pH=pH, cond=cond)
		new_obj.save()

	# Render the HTML template with the data in the context variable
	return render(request, "index.html")

from django.contrib.auth import get_user_model
User = get_user_model()

def send_warning_signal(request, id): # POST Request to turn on LEDs
	user = User.objects.all()[0]

	sensor = user.sensor

	ip_addr = sensor.ip_addr
	port = sensor.port

	post_data = {'valve': False, 'LED' : True}

	# replace this with IP address and port number of client sensors
	response = requests.post(f'http://{ip_addr}:{port}', data=post_data)
	content = response.content

	# Render the HTML template with the data in the context variable
	return render(request, "index.html")