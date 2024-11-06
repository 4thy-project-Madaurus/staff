from django.urls import path

from rest_framework import routers

from .views import TeacherViewSet, CreateManyTeachersView

router = routers.SimpleRouter()

router.register(r'', TeacherViewSet)

urlpatterns = [
    path('many/', CreateManyTeachersView.as_view(), name='create_many_teachers'),
]

urlpatterns += router.urls
