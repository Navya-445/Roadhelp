from django.contrib import admin

# Register your models here.


from .models import Customer, Mechanic
from .models import Customer, Mechanic, MechanicProfile, ServiceProvided, ServiceRequest, TaskAssignment,SparePart, MechanicTaskUpdate

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile', 'address')

@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile', 'skill', 'status')

from django.contrib import admin
from .models import ServiceProvided, ServiceRequest

@admin.register(ServiceProvided)
class ServiceProvidedAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description')

# Service Request Admin
@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'name', 'email', 'contact_number', 'location', 'state', 'city', 'vehicle_reg_number')
    search_fields = ('user__username', 'name', 'email', 'contact_number', 'vehicle_reg_number')
    list_filter = ('state', 'city')

# Mechanic Profile Admin
@admin.register(MechanicProfile)
class MechanicProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'contact_no', 'experience', 'specialization', 'district')
    search_fields = ('first_name', 'last_name', 'email', 'specialization__name', 'district')
    list_filter = ('district', 'specialization')

# Task Assignment Admin
@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_request', 'mechanic', 'status', 'assigned_date')
    list_filter = ('status', 'mechanic__district')
    search_fields = ('user__username', 'service_request__name', 'mechanic__first_name', 'mechanic__last_name')

from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created_at',)
from .models import MechanicNum

@admin.register(MechanicNum)
class MechanicNumAdmin(admin.ModelAdmin):
    list_display = ('id', 'Mob_num')  # Display fields in the admin panel
    search_fields = ('Mob_num',)  # Add search functionality
@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'stock_quantity')

@admin.register(MechanicTaskUpdate)
class MechanicTaskUpdateAdmin(admin.ModelAdmin):
    list_display = ('task', 'status', 'location_reached_time', 'service_completed_time')
    list_filter = ('status',)


