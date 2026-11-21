from django.contrib import admin
from .models import TestKit, TestEvent


@admin.register(TestKit)
class TestKitAdmin(admin.ModelAdmin):
    list_display = ('name', 'catalogue_reference', 'manufacturer', 'category', 'active')
    list_filter = ('active', 'category', 'manufacturer')
    search_fields = ('name', 'catalogue_reference', 'manufacturer')


@admin.register(TestEvent)
class TestEventAdmin(admin.ModelAdmin):
    list_display = ('sample', 'kit', 'result_category', 'performed_at', 'performed_by', 'kit_lot_number', 'kit_expiry_date')
    list_filter = ('result_category', 'kit', 'performed_at')
    search_fields = ('sample__sample_code', 'kit__name', 'kit_lot_number', 'observation_notes')
    readonly_fields = ('created_at',)
    date_hierarchy = 'performed_at'
