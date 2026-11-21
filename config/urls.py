"""
URL configuration for drug_field_companion project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('cases.urls')),
    path('', include('testing_records.urls')),
    path('', include('custody.urls')),
    path('', include('evidence.urls')),
    path('', include('reviews.urls')),
    path('', include('auditlog.urls')),
]

handler403 = 'core.views.custom_permission_denied_view'
handler404 = 'core.views.custom_page_not_found_view'
handler500 = 'core.views.custom_server_error_view'
