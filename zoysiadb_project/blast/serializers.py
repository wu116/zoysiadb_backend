from rest_framework import serializers
from .models import BlastDBFILE

class BlastDBFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlastDBFILE
        fields = ['id', 'file_type', 'file_name', 'file_path', 'created_at']