import json

from django.contrib.auth  import get_user_model, authenticate
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from ..utils import create_permit_user
from .serializers import ResetPasswordSerializer, LoginSerializer, MyTokenObtainPairSerializer,UserSerializer, UpdatePasswordSerializer
from authentication.models import OTP
from .utils import gen_otp
from rest_framework.viewsets import ModelViewSet
from threading import Thread
from kafka_runner.producer import kafka_produce
from ..interfaces import UserClaim
from ..permissions import   IsAdminUser
User = get_user_model()



    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class AuthTest(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"msg":"auth confirmed"})
    


class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            otp = OTP.objects.filter(user=user).first()
            if otp:
                otp.delete()
            code = gen_otp()
            OTP.objects.create(code=code, user=user)
            send_mail(
                'Reset Password OTP',
                f'Your OTP is {code}',
                'shannachi2@gmail.com',
                [email],
                fail_silently=False,
            )
            return Response({'message':'OTP code sent successfully'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error':'No such user found with this email!'}, status=status.HTTP_404_NOT_FOUND)

class AdminLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_staff and user.is_superuser:
                    token_serializer = MyTokenObtainPairSerializer()
                    token = token_serializer.get_token(user)
                    response = Response({'refresh':str(token), 'access': str(token.access_token)}, status=status.HTTP_200_OK)
                    response.set_cookie(
                        key="refresh_token",
                        value=str(token),
                        expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                        secure=settings.SIMPLE_JWT["SECURE"],
                        httponly=settings.SIMPLE_JWT["HTTPONLY"],
                        samesite=settings.SIMPLE_JWT["SAMESITE"]
                    )
                    return response
                return Response({'error':'User is not an admin'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'error':'User not found'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error':'Data not valid'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        otp.delete()
        user = serializer.validated_data['user']
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({'message': 'Password reset successfully'}, status=status.HTTP_202_ACCEPTED)




class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def profile(self, request, id=None):
        user = self.get_object()
        is_student = hasattr(user, 'student')
        if is_student:
            contributions = user.student.contributions.all()
            data = {
                'username': user.username,
                'email': user.email,
                "bio": user.bio,
                "birth_date": user.birth_date,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "avatar": user.avatar.url if user.avatar else "",
                "city": user.city,
                "gender": user.gender,
                "phone": user.phone_number,
                'contributions': [
                    {
                        'commits': contribution.commits,
                        'created_at': contribution.created_at
                    }
                    for contribution in contributions
                ],
                "group": user.student.group,
                "promo": user.student.promo,
                "year": user.student.year,
            }
        else:
            data = {
                'username': user.username,
                'email': user.email,
                "bio": user.bio,
                "birth_date": user.birth_date,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "avatar": user.avatar.url if user.avatar else "",
                "city": user.city,
                "gender": user.gender,
                "phone": user.phone_number,
            }

        return Response(data, status=status.HTTP_200_OK)
    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
       # self.check_permissions(request)
        return super().destroy(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        user =  UserClaim(
            username=response.data['username'],
            email=response.data['email'],
            role=response.data['role'],
            id=response.data['id'],
            avatar=response.data['avatar'],
            group=response.data['group'],
            year=response.data['year']
        )
        userStringify = json.dumps(user,separators=(',', ':'))
        kafka_produce("user",userStringify)
        return response


    def create(self, request, *args, **kwargs):
        """
        This function made only the creating admin user
        """
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        response = super().create(request, *args, **kwargs)
        print(response.data)
        user = {
            "id": response.data.get("id"),
            "first_name": response.data.get("first_name"),
            "last_name": response.data.get("last_name"),
            "email": response.data.get("email"),
            "role":"admin"
        }

        thread = Thread(target=create_permit_user, args=[user])
        # handle the thread
        thread.start()
        return response




class UpdatePasswordView(generics.UpdateAPIView):
    """
    An endpoint for updating the user's password.
    """
    serializer_class = UpdatePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Call serializer's update method
            serializer.update(self.object, serializer.validated_data)
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)