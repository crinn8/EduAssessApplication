from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from courses.api.serializers import CourseSerializer, CourseReadOnlySerializer, CourseFileSerializer
from courses.filters import CourseApiFilter, CourseFileApiFilter
from courses.models import Course, CourseFile
from django.db.models import Q

from quizes.api.serializers import QuizSerializer
from quizes.filters import QuizApiFilter
from quizes.models import Quiz, DeliveredQuiz


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    model = Course
    queryset = Course.objects.all()
    filterset_class = CourseApiFilter


class CourseListAPIView(ListAPIView):
    serializer_class = QuizSerializer
    model = Quiz
    queryset = Quiz.objects.all()

    # filterset_class = QuizApiFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Quiz.objects.filter(courses__id=self.request.GET.get('id'), )
        delivered_quizzes = DeliveredQuiz.objects.filter(student=user, course__id=self.request.GET.get('id')).values(
            'quiz')

        return queryset.exclude(id__in=delivered_quizzes)


class CourseFileViewSet(ModelViewSet):
    serializer_class = CourseFileSerializer
    model = CourseFile
    queryset = CourseFile.objects.all()
    filterset_class = CourseFileApiFilter
