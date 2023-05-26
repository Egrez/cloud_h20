from django.shortcuts import render

# Create your views here.
def home(request):
    sensors = [{'name': 'TDS sensor', 'state': 'potable'},
               {'name': 'pH sensor', 'state': 'nonpotable'}]
    return render(request, "index.html", {'sensors': sensors})