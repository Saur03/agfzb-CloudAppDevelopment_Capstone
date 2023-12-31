# djangoapp/admin.py
from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Number of empty forms to display for adding related CarModel objects

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('car_make', 'name', 'car_type', 'year', 'dealer_id')  # Customize the fields displayed in the admin list view

