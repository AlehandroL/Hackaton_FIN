from django.contrib import admin

from .models import Request, Offer


@admin.register(Request)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'start_time', 'end_time', 'message', 'active']
    list_editable = ['date', 'start_time', 'end_time', 'message', 'active']


@admin.register(Offer)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'start_time', 'end_time', 'message', 'active']
    list_editable = ['date', 'start_time', 'end_time', 'message', 'active']
