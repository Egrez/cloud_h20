from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('warn', views.send_warning_signal, name='warn'),
    path('stop/warn', views.send_stop_warning_signal, name='stop-warn'),
    path('signin', views.signin, name='signin'),
    path('auto', views.auto, name='auto'),
]
