from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.review_list_view, name='review_list'),
    path('reviews/<int:case_id>/', views.review_create_view, name='review_create'),
]
