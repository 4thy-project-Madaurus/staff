from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from teachers.models import Teacher
from authentication.api.serializers import UserSerializer, SafeUserSerializer, DangUserSerializer

User = get_user_model()


class CreateTeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Teacher
        fields = ['id', 'user']
        read_only_fields = ('id',)
        
    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        print("start")
        # thread = threading.Thread(target=create_permit_user, args=(user_data,))
        # thread.start()
        # still not work
        # response = create_permit_user(user)
        # print(response)
        print("end")
        return teacher  

        
class UpdateTeacherSerializer(serializers.ModelSerializer):
    user = DangUserSerializer()
    
    class Meta:
        model = Teacher
        fields = ['id', 'user']
        read_only_fields = ('id',)
        
    def update(self, instance, validated_data):
        user_instance = instance.user
        user_serializer = self.fields['user']
        
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer.update(user_instance, user_data)
        return super().update(instance, validated_data)

class SafeTeacherSerializer(serializers.ModelSerializer):
    user = SafeUserSerializer()
    
    class Meta:
        model = Teacher
        fields = ['id', 'user']
        read_only_fields = ('id',)
        
class MinimalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']