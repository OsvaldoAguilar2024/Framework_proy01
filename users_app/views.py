from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # Add this import
from django.http import HttpResponse
from django.contrib.auth import logout
from .models import UserCompany # Add this import

app_name = 'users_app'
@login_required # Add this line
def select_company(request):
    user = request.user
    user_companies = UserCompany.objects.filter(user=user)  # Get all the UserCompany objects for this user.
    companies = [user_company.company for user_company in user_companies]  # extract the company object.

    if request.method == 'POST':
        company_id = request.POST.get('company')
        if company_id:
            request.session['selected_company_id'] = company_id
            return redirect('myapp:home')  # Redirect to the home page
        
    context = {
        'companies': companies
    }
    return render(request, 'select_company.html', context) # Change this line

def logout_view(request):
    if 'selected_company_id' in request.session:
        del request.session['selected_company_id']
    logout(request)
    return render(request, 'logout.html') #this is the change
