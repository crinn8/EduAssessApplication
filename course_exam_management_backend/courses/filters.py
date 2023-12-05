from django_filters import rest_framework as filters, FilterSet, CharFilter
from courses.models import Course, CourseFile


class CourseApiFilter(filters.FilterSet):
    class Meta:
        model = Course
        fields = {
            "id": ['exact'],
            "classes__students__id": ['exact'],
        }


class CourseFileApiFilter(filters.FilterSet):
    class Meta:
        model = CourseFile
        fields = {
            "id": ['exact'],
            "course__id": ['exact'],
        }
