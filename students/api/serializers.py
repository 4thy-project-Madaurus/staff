from django.contrib.auth import get_user_model

from rest_framework import serializers

from students.models import Student
from authentication.api.serializers import UserSerializer, SafeUserSerializer, DangUserSerializer

User = get_user_model()

# class PromoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Promo
#         fields = ['study_year']
        
        
# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['id', 'group', 'promo']

class CreateStudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'group', 'promo', 'year', 'registration_number', 'promo_group']
        read_only_fields = ('id',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            student = Student.objects.create(user=user, **validated_data)
            return student
        else:
            raise serializers.ValidationError("Error creating user")
        
class UpdateStudentSerializer(serializers.ModelSerializer):
    user = DangUserSerializer() 

    class Meta:
        model = Student
        fields = ['user', 'group', 'promo', 'year', 'registration_number', 'promo_group']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})  
        user_serializer = self.fields['user'] 
        user_instance = instance.user  

        if user_data:
            user_serializer.update(user_instance, user_data)

        instance.group = validated_data.get('group', instance.group)
        instance.year = validated_data.get('year', instance.year)
        instance.promo = validated_data.get('promo', instance.promo)
        instance.registration_number = validated_data.get('registration_number', instance.registration_number)
        user_instance.save()
        instance.save()

        return instance

# class UpdateStudentSerializer(serializers.ModelSerializer):
#     user_email = serializers.EmailField(source='user.email')
#     user_first_name = serializers.CharField(source='user.first_name')
#     user_last_name = serializers.CharField(source='user.last_name')

#     class Meta:
#         model = Student
#         fields = ['user_email', 'user_first_name', 'user_last_name', 'group', 'promo', 'year', 'registration_number']

#     def update(self, instance, validated_data):
#         instance.group = validated_data.get('group', instance.group)
#         instance.year = validated_data.get('year', instance.year)
#         instance.promo = validated_data.get('promo', instance.promo)
#         instance.registration_number = validated_data.get('registration_number', instance.registration_number)
        
#         user_data = validated_data.get('user', {})
#         user = instance.user
#         user_email = user_data.get('email')
#         if user_email:
#             user.email = user_email
#         user_first_name = user_data.get('first_name')
#         if user_first_name:
#             user.first_name = user_first_name
#         user_last_name = user_data.get('last_name')
#         if user_last_name:
#             user.last_name = user_last_name

#         user.save()
#         instance.save()
#         return instance
    
class SafeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'birth_date', 'avatar_url', 'city', 'gender']
 
class SafeStudentSerializer(serializers.ModelSerializer):
    user = SafeUserSerializer()

    

    class Meta:
        model = Student
        fields = ['user', 'group', 'year', 'promo', 'registration_number', 'promo_group']
        # read_only_fields = ('id',)
        
