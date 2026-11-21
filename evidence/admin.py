from django.contrib import admin
from .models import EvidenceFile


@admin.register(EvidenceFile)
class EvidenceFileAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'case', 'sample', 'file_size_display', 'content_type', 'uploaded_by', 'uploaded_at')
    list_filter = ('content_type', 'uploaded_at')
    search_fields = ('original_filename', 'caption', 'case__case_reference', 'sample__sample_code')
    readonly_fields = ('uploaded_at', 'file_size', 'content_type', 'original_filename')
