from django.contrib import admin
from .models import*
admin.site.register([
    ordonnance,consultation,medicament,medecin,patient
])
