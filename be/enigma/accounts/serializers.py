from rest_framework import serializers
from .models import User, EmailVerificationToken
from .models import phone_regex

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'telephoneNumber', 'terms', 'privacy', 'newsletter']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user