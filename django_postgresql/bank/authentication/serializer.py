from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'],
            password=attrs['password']
        )

        if not user:
            return serializers.ValidationError('Invalid Credentials')
        
        token = RefreshToken.for_user(user)

        return {
            'access': str(token.access_token),
            'refresh': str(token),
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }
