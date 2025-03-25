from django.urls import path
from . import views

urlpatterns = [
    path('api/blast/', views.blast_request, name='blast-api'),
    path('api/get_blastdb/', views.get_blastdb.as_view(), name='get_blastdb-api'),
]