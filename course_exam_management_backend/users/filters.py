from django_filters import rest_framework as filters, FilterSet, CharFilter
from users.models import User


class UserApiFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            "is_student": ['exact'],
            "classes__courses__id": ['exact'],
        }
