# myapp/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm # Import AuthenticationForm
from semantic_forms.forms import SemanticForm # Import SemanticForm
from django.utils.translation import gettext_lazy as _


class CustomAdminLoginForm(AuthenticationForm, SemanticForm):
    """
    A custom login form for the admin that integrates with Semantic UI.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize the username field
        self.fields['username'].widget.attrs['placeholder'] = _('Enter your username')
        self.fields['username'].label = _('Username')

        # Customize the password field
        self.fields['password'].widget.attrs['placeholder'] = _('Enter your password')
        self.fields['password'].label = _('Password')
    




