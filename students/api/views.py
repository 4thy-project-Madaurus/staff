from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import   CreateStudentSerializer, SafeStudentSerializer, UpdateStudentSerializer
from students.models import  Student
from django.db.models import Value, CharField, F, Q
from threading import Thread
from django.conf import settings
from authentication.interfaces import UserClaim
import json
from kafka_runner.producer import kafka_produce
from authentication.utils import create_permit_user
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import Concat

# import logging

# logger = logging.getLogger(__name__)

# class PromoViewSet(viewsets.ModelViewSet):
#     queryset = Promo.objects.all()
#     serializer_class = PromoSerializer
    
# class GroupViewSet(viewsets.ModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
    

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = SafeStudentSerializer
    lookup_field = 'user_id'
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateStudentSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateStudentSerializer  
        elif self.action == 'list':
            return SafeStudentSerializer
        return self.serializer_class
    
    def create(self, request, *args, **kwargs):
        # self.permission_classes = [IsAdminUser]
        #self.check_permissions(request)
        response = super().create(request, *args, **kwargs)
        data = response.data
        user = {
            "id": response.data.get("id", None),
            "first_name": data.get("user").get("first_name", None),
            "last_name": data.get("user").get("last_name", None),
            "email": data.get("user").get("email", None),
            "role": "student",
            "promo": data.get("promo", None),
        }
        thread = Thread(target=create_permit_user, args=[user])
        thread.start()
        return response
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        data = response.data["user"]
        student = Student.objects.filter(user__email=data["email"]).first()
        user = UserClaim(
            username=data.get('username', None),
            email=data.get('email', None),
            role="student",
            id=data.get('id', None),
            avatar=data.get('avatar_url', None),
            group=student.group,
            year=student.year,

        )
        userStringify = json.dumps(user, separators=(',', ':'))
        thread = Thread(target=kafka_produce, args=[settings.USER_MUTATION_TOPIC, userStringify])
        thread.start()
        # kafka_produce(settings.USER_MUTATION_TOPIC, userStringify)
        return response


    
class CreateManyStudentsView(APIView):
    serializer_class = CreateStudentSerializer  
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GroupsViewSet(viewsets.ViewSet):
#     def list(self, request):
#         groups = (
#             Student.objects
#             .annotate(group_name=Concat('promo', Value('-'), 'group', output_field=CharField()))
#             .values_list('group_name', flat=True)
#             .distinct()
#             .exclude(group_name__isnull=True)
#         )
#         groups_list = list(groups)
#         return Response(groups_list)


class GroupsViewSet(viewsets.ViewSet):
    def list(self, request):
        groups = Student.objects.filter(~Q(group__isnull=True) & ~Q(group='')).values_list('group', flat=True).distinct()
        groups_list = list(groups)
        return Response(groups_list)

class PromosViewSet(viewsets.ViewSet):
    def list(self, request):
        promos = Student.objects.filter(~Q(promo__isnull=True) & ~Q(promo='')).values_list('promo', flat=True).distinct()
        promos_list = list(promos)
        return Response(promos_list)

class YearsViewSet(viewsets.ViewSet):
    def list(self, request):
        years = Student.objects.filter(~Q(year__isnull=True) & ~Q(year='')).values_list('year', flat=True).distinct()
        years_list = list(years)
        return Response(years_list)

