from django.urls import path
from . import views

urlpatterns = [
    path('cases/<int:case_id>/evidence/upload/', views.evidence_upload_view, name='evidence_upload'),
    path('evidence/<int:pk>/download/', views.evidence_download_view, name='evidence_download'),
]
