from django.db import models
from django.contrib.auth import get_user_model
# from django.contrib.postgres.fields import ArrayField



from utils.models import  UUIDModel
# from students.api.serializers import StudentSerializer

User = get_user_model()
# Create your models here.

# class Group(UUIDModel):
#     group  = models.CharField(max_length=255)
#     promo = models.CharField(max_length=255)
    
class Student(UUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    group = models.CharField(max_length=255, null=True, blank=True)
    promo = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255, null=True, blank=True)
    registration_number = models.CharField(max_length=255,  null=True, blank=True)
    @property
    def promo_group(self):
        return f"{self.promo}-{self.group}" 
    
    def get_group_name(self):
        print("hello")
        return f"{self.year}-{self.group}"
    
    # def save(self, *args, **kwargs):
    #     if self.group and self.year:
    #         self.valid_group = f"{self.year}-{self.group}"
    #     super().save(*args, **kwargs)
    
    
