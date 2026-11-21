from django.contrib import admin
from .models import CaseRecord, Sample


class SampleInline(admin.TabularInline):
    model = Sample
    extra = 0
    fields = ('sample_code', 'collected_at', 'initial_condition', 'packaging_reference', 'seal_reference')
    readonly_fields = ('sample_code',)


@admin.register(CaseRecord)
class CaseRecordAdmin(admin.ModelAdmin):
    list_display = ('case_reference', 'title', 'status', 'incident_datetime', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('status', 'incident_datetime', 'created_at')
    search_fields = ('case_reference', 'title', 'general_location', 'description')
    readonly_fields = ('case_reference', 'created_at', 'updated_at')
    date_hierarchy = 'incident_datetime'
    inlines = [SampleInline]


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ('sample_code', 'case', 'collected_at', 'packaging_reference', 'seal_reference', 'initial_condition', 'created_by')
    list_filter = ('collected_at', 'created_at')
    search_fields = ('sample_code', 'description', 'packaging_reference', 'seal_reference', 'case__case_reference')
    readonly_fields = ('sample_code', 'created_at')
    date_hierarchy = 'collected_at'
