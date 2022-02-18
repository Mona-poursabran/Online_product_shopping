from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display =['name', 'price', 'digital']
    list_display_links= ['name', 'price']
    list_filter= ['digital']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['id', 'product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['complete', 'id', 'customer']
    list_filter = ['complete']


admin.site.register(Address)
# admin.site.register(Customer)