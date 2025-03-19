

from django.urls import path
from users_app import views
from django.contrib.auth.views import LoginView # change this line to import LoginView
 
 

app_name = 'users_app'

urlpatterns = [
    path('login', LoginView.as_view(template_name='login.html'), name='login'), #change this line to use LoginView
    path('logout/', views.logout_view , name='logout'),
    path('select-company/', views.select_company, name='select_company'),

    
]