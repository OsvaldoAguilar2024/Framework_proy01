# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from myapp.models import Empresa  # Import Empresa

class UserCompany(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    company = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    def __str__(self):
        return self.company.nombreempresa # Add this line, we need to show the company name.


class CustomUser(AbstractUser):
    Empresa = models.ManyToManyField(Empresa, through='UserCompany', related_name='usuarios', blank=True) #change the name
    # Add more fields as needed...

    # You can override existing methods or add new ones.
    # For example:
    def get_full_info(self):
        return f"{self.first_name} {self.last_name} - {self.Empresa}"

    def __str__(self):
        return self.username

