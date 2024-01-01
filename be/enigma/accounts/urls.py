from django.urls import path
from . import views
from .views import *

app_name = "accounts"

urlpatterns = [
    ##### LOGIN #####
    path('login', views.login),
    ##### REGISTRATION ######
    path('registration', views.registration),
    ##### VERIFY REGISTRATION EMAIL #####
    path('verify-email/<uuid:token>', views.verifyRegistrationEmail, name='verifyRegistrationEmail'),
    ##### RECOVERY PASSWORD #####
    ##### TEST #####
    #path('test', views.test),
]