from django.shortcuts import render
from sensors.models import Sensors, ServerData

# Create your views here.
def home(request):
    return render(request, "index.html")

def sensor(request): # POST Request for Sensor Readings
    device_id = request.POST['device_id']
    location = request.POST['location']
    data = request.POST['data']

    #Timestamp should be automatically assigned when saved
    new_obj = Sensors(device_id=device_id, location=location, data=data)
    new_obj.save()

    # Render the HTML template with the data in the context variable
    return render(request, "index.html")
