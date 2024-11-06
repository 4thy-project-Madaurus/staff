from django.urls import path
from .views import MyTokenObtainPairView, SendOTPView, ResetPasswordView, AuthTest, AdminLoginView,UserViewSet, UpdatePasswordView
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)


urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('admin-login/',AdminLoginView.as_view() , name='admin-login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path("auth-test/", AuthTest.as_view(), name="auth-test"),
    path("send-otp/", SendOTPView.as_view(), name="send-otp"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path('update-password/', UpdatePasswordView.as_view(), name='password_update'),
]

urlpatterns += router.urls