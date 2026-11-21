from django.urls import path
from . import views

urlpatterns = [
    path('samples/<int:sample_id>/tests/new/', views.test_event_create_view, name='test_event_create'),
    path('kits/', views.kit_list_view, name='kit_list'),
    path('kits/new/', views.kit_create_view, name='kit_create'),
    path('kits/<int:pk>/edit/', views.kit_edit_view, name='kit_edit'),
]
