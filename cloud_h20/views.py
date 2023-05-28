from django.shortcuts import render
from sensors.models import Sensors

# Create your views here.
def home(request):
    sensors = Sensors.objects.all()
    return render(request, "index.html", {'sensors': sensors})