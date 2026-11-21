from django.urls import path
from . import views

urlpatterns = [
    path('cases/', views.case_list_view, name='case_list'),
    path('cases/new/', views.case_create_view, name='case_create'),
    path('cases/<int:pk>/', views.case_detail_view, name='case_detail'),
    path('cases/<int:pk>/edit/', views.case_edit_view, name='case_edit'),
    path('cases/<int:pk>/submit/', views.case_submit_view, name='case_submit'),
    path('cases/<int:pk>/report/', views.case_report_view, name='case_report'),
    path('cases/<int:case_id>/samples/new/', views.sample_create_view, name='sample_create'),
    path('samples/<int:pk>/', views.sample_detail_view, name='sample_detail'),
    path('samples/<int:pk>/edit/', views.sample_edit_view, name='sample_edit'),
]
