from django.db import models


from students.models import Student
# Create your models here.



class StudentScore(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="scores")
    # should be positive
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.student} - {self.evaluation} - {self.score}"



class Contribution(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="contributions")
    commits = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.student} - {self.commits}"
    # student_id and created_at should be unique together
    class Meta:
        unique_together = ['student', 'created_at']