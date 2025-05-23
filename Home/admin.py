from django.contrib import admin

# Register your models here.

from .models import MechanicDetailsFill
from .models import Customer, Mechanic
from .models import Customer, Mechanic, MechanicProfile, ServiceProvided, ServiceRequest, TaskAssignment,SparePart, MechanicTaskUpdate, StatusUpdate

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
@admin.register(StatusUpdate)
class StatusUpdateAdmin(admin.ModelAdmin):
    list_display = ['task', 'mechanic', 'service_request', 'status', 'updated_at']
@admin.register(MechanicDetailsFill)
class MechanicDetailsAdmin(admin.ModelAdmin):
    list_display = ('task', 'mechanic', 'completed_date', 'reached_time', 'finished_time', 'total_duration')
    search_fields = ('task__id', 'mechanic__user__username')
    list_filter = ('completed_date',)
from .models import Feedback
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_request', 'mechanic', 'overall_experience', 'submitted_at')
    search_fields = ('name', 'service_request__service', 'mechanic__first_name', 'mechanic__last_name')
    list_filter = ('overall_experience', 'submitted_at')
from django.contrib import admin
from .models import MechanicAlertStatus,PaymentInfo

@admin.register(MechanicAlertStatus)
class MechanicAlertStatusAdmin(admin.ModelAdmin):
    list_display = ('mechanic', 'alert_status')  # Show mechanic name and alert status
    list_filter = ('alert_status',)  # Allow filtering by alert status
    search_fields = ('mechanic__user__username',)  # Search by mechanic's username
from .models import ServiceProvided, PriceList
@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ('service', 'amount_inr')
    search_fields = ('service__name',)
    list_filter = ('service',)
@admin.register(PaymentInfo)
class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'service_request', 'amount', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('customer_name', 'mobile_number', 'order_id', 'payment_id')
    readonly_fields = ('created_at', 'order_id', 'payment_id')

    def get_readonly_fields(self, request, obj=None):
        """ Make certain fields read-only after payment is completed. """
        if obj and obj.is_paid:
            return self.readonly_fields + ('amount', 'is_paid')
        return self.readonly_fields
from django.contrib import admin
from .models import CustPayment

from django.contrib import admin
from .models import CustPayment

@admin.register(CustPayment)
class CustPaymentAdmin(admin.ModelAdmin):
    list_display = ("service_request_name", "cust_name", "amount_paid", "is_paid", "order_id")  # Added order_id
    list_filter = ("is_paid",)  # Filter by payment status
    search_fields = ("cust_name", "service_request_name", "order_id")  # Added order_id to search
    actions = ["mark_as_paid"]

    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True)
    mark_as_paid.short_description = "Mark selected payments as Paid"
