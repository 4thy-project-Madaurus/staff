from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from threading import Thread
from .serializers import CreateTeacherSerializer, SafeTeacherSerializer, UpdateTeacherSerializer, MinimalUserSerializer
from teachers.models import Teacher
from authentication.utils import create_permit_user
from authentication.interfaces import UserClaim
from authentication.models import User
import json
from kafka_runner.producer import kafka_produce

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = SafeTeacherSerializer
    lookup_field = 'user_id'
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTeacherSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateTeacherSerializer
        elif self.action == 'list':
            return SafeTeacherSerializer
        return self.serializer_class
    def create(self, request, *args, **kwargs):
        # self.permission_classes = [IsAdminUser]
        #self.check_permissions(request)
        response = super().create(request, *args, **kwargs)
        print(response.data)
        user = {
            "id": response.data.get("id"),
            "first_name": response.data.get("user").get("first_name"),
            "last_name": response.data.get("user").get("last_name"),
            "email": response.data.get("user").get("email"),
            "role": "teacher"
        }
        thread = Thread(target=create_permit_user, args=[user])
        thread.start()
        return response
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        data = response.data["user"]
        teacher = Teacher.objects.filter(user__email=data["email"]).first()
        user = UserClaim(
            username=data.get('username', None),
            email=data.get('email', None),
            role="teacher",
            id=data.get('id', None),
            avatar=data.get('avatar_url', None),
        )
        userStringify = json.dumps(user, separators=(',', ':'))
        thread = Thread(target=kafka_produce, args=[settings.USER_MUTATION_TOPIC, userStringify])
        thread.start()
        # kafka_produce(settings.USER_MUTATION_TOPIC, userStringify)
        return response
    
 
class TeacherListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = MinimalUserSerializer
    permission_classes = [IsAuthenticated]

class CreateManyTeachersView(APIView):
    serializer_class = CreateTeacherSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
