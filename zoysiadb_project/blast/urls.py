from django.urls import path
from . import views

urlpatterns = [
    path('api/blast/', views.blast_request, name='blast-api'),
]