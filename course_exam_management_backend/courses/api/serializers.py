from rest_framework import serializers

from courses.models import Course, CourseFile


class CourseFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFile
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    quiz_detail = serializers.SerializerMethodField(read_only=True)
    classes_detail = serializers.SerializerMethodField(read_only=True)
    course_files = CourseFileSerializer(read_only=True, many=True, source='coursefile_set')

    def get_quiz_detail(self, obj):
        from quizes.api.serializers import QuizSerializer
        return QuizSerializer(obj.quiz, many=True).data

    def get_classes_detail(self, obj):
        from classes.api.serializers import ClassSerializer
        return ClassSerializer(obj.classes, many=True).data

    class Meta:
        model = Course
        fields = "__all__"


class CourseReadOnlySerializer(serializers.ModelSerializer):
    # quiz = QuizSerializer(many=True, read_only=True)
    quiz = serializers.SerializerMethodField(read_only=True)
    course_files = CourseFileSerializer(read_only=True, many=True, source='coursefile')

    def get_quiz(self, obj):
        from quizes.api.serializers import QuizSerializer
        return QuizSerializer(obj.quiz, many=True).data

    class Meta:
        model = Course
        fields = "__all__"
