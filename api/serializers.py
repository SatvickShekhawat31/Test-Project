from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UploadedFile

User = get_user_model()

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'uploaded_at', 'uploader']
        read_only_fields = ['uploader', 'uploaded_at']  # 👈 uploader & uploaded_at ko readonly rakha

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],   # 👈 directly le rahe hain
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user
