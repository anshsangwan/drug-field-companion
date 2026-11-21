from django.contrib import admin
from .models import ReviewRecord


@admin.register(ReviewRecord)
class ReviewRecordAdmin(admin.ModelAdmin):
    list_display = ('case', 'reviewer', 'decision', 'reviewed_at')
    list_filter = ('decision', 'reviewed_at')
    search_fields = ('case__case_reference', 'reviewer__username', 'comment')
    readonly_fields = ('reviewed_at',)
    date_hierarchy = 'reviewed_at'
