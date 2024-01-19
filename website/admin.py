from django.contrib import admin
from .models import Record, Product, Service, Order

models = [Record, Product, Service, Order]

admin.site.register(models)
