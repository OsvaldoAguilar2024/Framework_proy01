# myapp/urls.py
from django.urls import include, path
from . import views
from django.conf.urls import handler403 , handler404 , handler500 ,handler400



app_name = 'myapp'  # This is the crucial line we're adding!

urlpatterns = [
    path('', views.home, name='home'),
    path('error/', views.mi_pagina_de_error, name='mi_pagina_de_error'),  
]


