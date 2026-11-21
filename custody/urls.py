from django.urls import path
from . import views

urlpatterns = [
    path('samples/<int:sample_id>/custody/new/', views.custody_event_create_view, name='custody_event_create'),
    path('samples/<int:sample_id>/custody/timeline/', views.custody_timeline_view, name='custody_timeline'),
]
