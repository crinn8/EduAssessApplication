from rest_framework.viewsets import ModelViewSet

from classes.api.serializers import ClassSerializer
from classes.models import Class


class ClassViewSet(ModelViewSet):
    serializer_class = ClassSerializer
    model = Class
    queryset = Class.objects.all()
