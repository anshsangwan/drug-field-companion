from django.contrib import admin
from .models import CustodyEvent


@admin.register(CustodyEvent)
class CustodyEventAdmin(admin.ModelAdmin):
    list_display = ('sample', 'event_type', 'event_at', 'from_person', 'to_person', 'location_reference', 'seal_reference', 'is_out_of_sequence', 'recorded_by')
    list_filter = ('event_type', 'is_out_of_sequence', 'event_at')
    search_fields = ('sample__sample_code', 'from_person', 'to_person', 'location_reference', 'seal_reference', 'remarks')
    readonly_fields = ('created_at',)
    date_hierarchy = 'event_at'
