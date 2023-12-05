from rest_framework import serializers

from classes.models import Class
from users.api.serializers import UserSerializer


class ClassSerializer(serializers.ModelSerializer):
    students_detail = UserSerializer(many=True, read_only=True, source='students')

    class Meta:
        model = Class
        fields = "__all__"
