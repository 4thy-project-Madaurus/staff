from django.db import models
from django.contrib.postgres.fields import ArrayField


from utils.models import UUIDModel
from authentication.models import User
# Create your models here.


class Teacher(UUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    # position = models.CharField(max_length=255, blank=True, null=True)
    # classes = ArrayField(
    #         models.CharField(max_length=255, blank=True, null=True),
    #         blank=True,
    #         null=True,
    #     )
    # courses = ArrayField(
    #         models.CharField(max_length=255, blank=True, null=True),
    #         blank=True,
    #         null=True,
    #     )