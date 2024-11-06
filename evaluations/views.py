from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from students.models import Student
from django.db.models import Sum
from .models import StudentScore
import random

class LeaderboardView(APIView):
    def get_leaderboard(self, start_date=None):
        if start_date:
            points = StudentScore.objects.filter(created_at__gte=start_date)
        else:
            points = StudentScore.objects.all()
        if points.exists():
            leaderboard = (
                points.values('student')  
                .annotate(total_points=Sum('score'))  
                .order_by('-total_points')
            )

            leaderboard_data = []
            rank = 1
            for entry in leaderboard:
                student = Student.objects.get(id=entry['student'])  
                leaderboard_data.append({
                    'student': student.user.username,
                    'group': student.group,
                    'promo': student.year,
                    'total_points': entry['total_points'],
                    'rank': rank,
                    'avatar_url': student.user.avatar_url
                })
                rank += 1

            return leaderboard_data
        else:
             # get random students
            random_students = list(Student.objects.all().order_by('?')[:10])  
            leaderboard_data = [{
                'student': student.user.username,
                'group': student.group,
                'promo': student.year,
                'total_points': 0,
                'rank': index + 1,
                'avatar_url': student.user.avatar_url
            } for index, student in enumerate(random_students)]

        return leaderboard_data

    def get(self, request):
        now = timezone.now()
        data = {
            'day': self.get_leaderboard(now - timedelta(days=1)),
            'week': self.get_leaderboard(now - timedelta(weeks=1)),
            'month': self.get_leaderboard(now - timedelta(days=30)),
            'all': self.get_leaderboard()
        }

        return Response({'data': data})


