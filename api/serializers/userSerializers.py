from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers, status
from rest_framework.validators import ValidationError
from ..utils import get_tokens
from ..models.users import CustomUser
from django.contrib.auth.hashers import make_password,check_password

"""
Serializer class for registering new user
"""
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only = True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only = True)
    
    class Meta:
        model = CustomUser
        fields = ['email','username','realname','password', 'password2']
        extra_kwargs = { 'password': {'write_only': True}, }
    
    def save(self):
        instance = self.Meta.model(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            realname = self.validated_data['realname'],
        )

        password = self.validated_data['password']
        instance.set_password(password)
        instance.save()
        return instance

"""
Serializer class for login
"""
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, min_length=1)
    password = serializers.CharField(max_length=68, min_length=1, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = CustomUser.objects.get(username=obj['username'])
        return get_tokens(user)

    class Meta:
        fields = ['username', 'password', 'tokens']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):

        username = attrs.get('username', '')
        password = attrs.get('password', '')
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid credentials, try again')
        elif not user.is_active:
            raise serializers.ValidationError('Account disabled, contact admin')
        elif user.isDeleted:
            raise serializers.ValidationError('Account deleted, contact admin')
        else:
            return {
                'username': user.username,
                'tokens': user.tokens
            }
        return None

"""
Serializer class for logout
"""
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.refresh = attrs['refresh']
        return attrs
    
    def save(self):
        try:
            RefreshToken(self.refresh).blacklist()
        except TokenError:
            raise AuthenticationFailed("Token Error. Might already be blacklisted.")


"""
Serializer for Create User
"""
class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'username','realname']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')


        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email is taken.")

        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Username is taken.")

    def save(self):
        instance = self.Meta.model(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        instance.save()
        return instance

"""
Serializer for List All Users
"""
class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'realname','email', 'profile']

class ListMemberSerializer(serializers.ModelSerializer):
    position = serializers.IntegerField()
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'realname','email', 'profile','position']
