from rest_framework import serializers
from .models import Mockup

class MockupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mockup
        fields = ['id', 'text', 'image', 'created_at']