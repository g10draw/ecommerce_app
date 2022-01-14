from django.contrib import admin

from .models import Order, OrderItem

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Attaches Order Control to Admin """
    list_display = [
        'id', 'first_name', 'last_name', 'email', 'mobile',
        'address', 'postal_code', 'city', 'created', 'status'
    ]
    list_filter = ['created', 'updated']

    inlines = [OrderItemInline]