import json

from channels.generic.websocket import WebsocketConsumer
from django.contrib.sessions.models import Session

from django.contrib.auth import get_user_model
User = get_user_model()

from sensors.models import SensorReading, Sensor


class SensorConsumer(WebsocketConsumer):

	groups = ["QC"]

	def connect(self):
		headers = dict(self.scope['headers'])

		session_id = headers[b'sessionid'].decode()

		session = Session.objects.get(session_key=session_id)

		session_data = session.get_decoded()

		user_id = session_data.get('_auth_user_id')
		user = User.objects.get(id=user_id)

		self.scope['user'] = user


		self.accept()

	# Receive message from the group
	def send_warning(self, text_data=""):
		user = self.scope['user']
		sensor = Sensor.objects.get(user_id=user.id)
		
		sensor.is_warning = True
		sensor.save()

		message = json.dumps({"LED" : "true"})

		# Send message to WebSocket
		self.send(text_data=message)

	# Receive message from the group
	def send_stop_warning(self, text_data=""):
		user = self.scope['user']
		sensor = Sensor.objects.get(user_id=user.id)

		sensor.is_warning = False
		sensor.save()
		
		message = json.dumps({"LED" : "false"})

		# Send message to WebSocket
		self.send(text_data=message)

	def disconnect(self, close_code):
		pass

	def receive(self, text_data):
		user = self.scope['user']
		sensor = Sensor.objects.get(user_id=user.id)

		text_data_json = json.loads(text_data)
		tds = text_data_json["tds"]
		pH = text_data_json["pH"]
		temp = text_data_json["temp"]

		is_safe_pH = True
		is_safe_temp = True
		is_safe_tds = True

		if pH < 6.5 or pH > 8.5:
			is_safe_pH = False
		if temp < 30 or temp > 35:
			is_safe_temp = False
		if tds > 600.6853818:
			is_safe_tds = False

		if not(is_safe_pH and is_safe_temp and is_safe_tds) and not(sensor.is_overriden) and not(sensor.is_warning):
			self.send_warning()
		elif is_safe_pH and is_safe_temp and is_safe_tds and not(sensor.is_overriden) and sensor.is_warning:
			self.send_stop_warning()

		new_obj = SensorReading(device_id=sensor, tds=tds, pH=pH, temp=temp, is_safe_tds=is_safe_tds, is_safe_pH=is_safe_pH, is_safe_temp=is_safe_temp)
		new_obj.save()