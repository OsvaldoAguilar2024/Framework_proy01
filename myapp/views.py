# myapp/views.py
from django.shortcuts import render, redirect
from .models import EjecucionMatriz, Empresa
from django.contrib.auth.decorators import login_required
from users_app.models import CustomUser
from django.contrib import messages
from django.http import QueryDict

@login_required
def home(request):
    """
    Displays the home page with the company logo of the logged-in user.
    """
    user = request.user
    #Check if a company is saved in the session.
    if  request.session.get('selected_company_id'):
        selected_company_id = request.session.get('selected_company_id')
        company = Empresa.objects.get(codigoempresa = selected_company_id)
        logo_url = company.logo.url if company and company.logo else None
    elif isinstance(user, CustomUser) and hasattr(user, 'Empresa') and user.Empresa.count() > 1 : # Change this line
        return redirect('users_app:select_company') # add the name space
    elif isinstance(user, CustomUser) and hasattr(user, 'Empresa') and  user.Empresa.count() == 1: # Change this line
        selected_company_id = user.Empresa.first().codigoempresa # Change this line
        request.session['selected_company_id'] = selected_company_id
        company = Empresa.objects.get(codigoempresa = selected_company_id)
        logo_url = company.logo.url if company and company.logo else None
    else:
        logo_url = None  # Or you can set a default logo here
        company = None
    

    context = {
        'company_name': company.nombreempresa if company else None,
        'logo_url': logo_url,
        'user': user
    }
    return render(request, 'home.html', context)



def mi_pagina_de_error(request, exception=None):
    return render(request, 'myapp/mi_pagina_de_error.html', {'exception': exception, 'error_code': 403})
