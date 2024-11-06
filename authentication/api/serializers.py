from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentication.models import OTP
from teachers.models import Teacher
from students.models import Student
from ..models import User


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise ValidationError({'error': 'Old password is incorrect'})
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'username', 'last_name', 'birth_date', 'avatar_url', 'city', 'phone_number', 'gender','bio')
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password field is write-only

    def update(self, instance, validated_data):
        validated_data.pop('password', None)  # Remove password from validated data
        validated_data.pop('role', None)  # Remove email from validated data
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
            password_data = validated_data.pop('password')
            user = User.objects.create(**validated_data)
            user.set_password(password_data)
            user.save()
            return user

class DangUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'birth_date', 'avatar_url', 'city', 'phone_number', 'gender')
        read_only_fields = ['id']

    def create(self, validated_data):
            password_data = validated_data.pop('password')
            user = User.objects.create(**validated_data)
            user.set_password(password_data)
            user.save()
            return user
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class SafeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'birth_date', 'avatar_url', 'gender', 'city', 'phone_number','bio')
        read_only_fields = ['id']
        
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['avatar'] = user.avatar_url if user.avatar_url else "default"
        
        teacher = Teacher.objects.filter(user__email=user.email)
        student = Student.objects.filter(user__email=user.email)
        token['username'] = user.username
        token['email'] = user.email
        if user.is_staff and user.is_superuser:
            token['role'] = "admin"
            token['group'] = "None"
            token['year'] = "None"
        elif teacher.exists():
            teacher = teacher.first()
            token['role'] = "teacher"
            token['group'] = "None"
            token['year'] = "None"
        elif student.exists():
            student = student.first()
            token['role'] = "student"
            token['group'] = str(student.group) if student.group else "None"
            token['year'] = str(student.year) if student.year else "None"
        else:
            raise ValidationError({'error': 'User has no role assigned'})
        return token

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, validators=[validate_password])
    code = serializers.CharField(required=True)


    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user:
            otp = OTP.objects.filter(user=user, code=data.get('code', None)).first()
            if otp:
                data['otp'] = otp
                data['user'] = user
                return data
        raise ValidationError({'error': 'something went wrong'})



        
    