from django.apps import AppConfig
from django.db import transaction
from django.conf import settings
import os

class BlastConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blast'

    def ready(self):
        if os.environ.get('RUN_MAIN') or not os.environ.get('DJANGO_AUTORELOAD'):
            from .models import BlastDBFILE
            try:
                BlastDBFILE.update_from_media()
                print("Successfully updated blast database records")
            except Exception as e:
                print(f"Failed to update blast DB: {str(e)}")
