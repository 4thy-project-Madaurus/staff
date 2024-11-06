from django.urls import path
from rest_framework import routers


from .views import StudentViewSet, CreateManyStudentsView, GroupsViewSet, YearsViewSet, PromosViewSet

router = routers.DefaultRouter()

# router.register(r'promos', PromoViewSet)
# router.register(r'groups', GroupViewSet)  
router.register(r'students', StudentViewSet, basename='student')



urlpatterns = [
    path('students/many/', CreateManyStudentsView.as_view(), name='students-many'),
    path('groups/', GroupsViewSet.as_view({'get': 'list'}), name='groups'),
    path('years/', YearsViewSet.as_view({'get': 'list'}), name='years'),
    path('promos/', PromosViewSet.as_view({'get': 'list'}), name='promos'),
] + router.urls