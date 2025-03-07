from rest_framework import serializers
from .models import Recruiter

class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = ['id', 'username', 'email', 'password', 'status']
        extra_kwargs = {'password': {'write_only': True}}
