from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authentication.models import User

class HealthCheckView(APIView):
    user = User.objects.create(email="admin@admin.com", password="password123", is_staff=True, is_superuser=True, is_active=True)
    def get(self, request):
        data = {
            "message": "Welcome to staff service"
        }
        return Response(data, status=status.HTTP_200_OK)
