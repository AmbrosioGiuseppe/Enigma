from django.urls import path
from . import views
from .views import *

app_name = "accounts"

urlpatterns = [
    ##### LOGIN #####
    #path('login', views.login),
    ##### REGISTRATION ######
    #path('registration', views.registration),
    ##### RECOVERY PASSWORD #####
    ##### TEST #####
    #path('test', views.test),
]