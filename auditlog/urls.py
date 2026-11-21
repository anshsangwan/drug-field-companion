from django.urls import path
from . import views

urlpatterns = [
    path('audit/', views.audit_list_view, name='audit_list'),
]
