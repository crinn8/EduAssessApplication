from django_filters import rest_framework as filters, FilterSet, CharFilter
from courses.models import Course
from quizes.models import DeliveredQuiz,Quiz


class DeliveredQuizApiFilter(filters.FilterSet):
    class Meta:
        model = DeliveredQuiz
        fields = {
            "course__id": ['exact'],
            "student__id": ['exact'],
            "quiz__id": ['exact'],
        }


class QuizApiFilter(filters.FilterSet):
    class Meta:
        model = Quiz
        fields = {
            # "course__id": ['exact'],
        }