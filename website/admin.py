from django.contrib import admin
from .models import Record, Product, Service

models = [Record, Product, Service]

admin.site.register(models)
