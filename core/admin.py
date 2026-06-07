from django.contrib import admin
from .models import Service, Staff, Booking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration', 'price']
    search_fields = ['name']
    list_filter = ['duration']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']
    filter_horizontal = ['specialization']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'service', 'staff', 'date', 'start_time', 'status']
    list_filter = ['status', 'date']