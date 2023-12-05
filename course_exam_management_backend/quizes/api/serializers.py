from rest_framework import serializers

from courses.api.serializers import CourseSerializer
from quizes.models import Quiz, QuizMcqs, QuizPythonProblem, QuizPythonProblemTestCase, DeliveredQuizMcqs, \
    DeliveredQuiz, DeliveredQuizPython, DeliveredQuizPythonTestCase, McqsCorrectAnswer, DeliveredMcqsAnswers
from django.db.models import Avg, Sum

from users.api.serializers import UserSerializer


class McqsCorrectAnswerSerializer(serializers.ModelSerializer):
    option1 = serializers.BooleanField(write_only=True, required=False)
    option2 = serializers.BooleanField(write_only=True, required=False)
    option3 = serializers.BooleanField(write_only=True, required=False)
    option4 = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = McqsCorrectAnswer
        fields = "__all__"


class QuizMcqsSerializer(serializers.ModelSerializer):
    correct_answers = McqsCorrectAnswerSerializer(many=True, source='mcqscorrectanswer_set')

    class Meta:
        model = QuizMcqs
        fields = "__all__"


class QuizPythonProblemTestCaseSerializer(serializers.ModelSerializer):
    # quiz_python_problem = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = QuizPythonProblemTestCase
        fields = "__all__"


class QuizPythonProblemSerializer(serializers.ModelSerializer):
    test_case = QuizPythonProblemTestCaseSerializer(many=True, source='quizpythonproblemtestcase_set')

    # quizpythonproblemtestcase_set = QuizPythonProblemTestCaseSerializer(many=True, read_only=True)

    # quiz = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = QuizPythonProblem
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    quizmcqs = QuizMcqsSerializer(many=True, write_only=True)
    quizmcqs_set = QuizMcqsSerializer(many=True, read_only=True)
    quizpythonproblem_set = QuizPythonProblemSerializer(many=True, read_only=True)
    quizpython = QuizPythonProblemSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Quiz
        fields = "__all__"

    def create(self, validated_data):
        quiz_mcqs_data = validated_data.pop('quizmcqs')
        quiz_python_data = validated_data.pop('quizpython')
        quiz = Quiz.objects.create(**validated_data)

        for quiz_mcq_data in quiz_mcqs_data:
            total_numbers = 0
            correct_answers = quiz_mcq_data.pop('mcqscorrectanswer_set')
            quiz_mcq_instance = QuizMcqs.objects.create(quiz=quiz, **quiz_mcq_data)

            total_true_options = [sub['option' + str(index + 1)] for (index, sub) in enumerate(correct_answers) if
                                  sub['option' + str(index + 1)] == True]

            for correct_answer in correct_answers:
                if correct_answer.pop('option1', False) or correct_answer.pop('option2', False) or correct_answer.pop(
                        'option3', False) or correct_answer.pop('option4', False):
                    correct_answer['numbers'] = quiz_mcq_instance.total_numbers / len(total_true_options)

                    McqsCorrectAnswer.objects.create(mcqs=quiz_mcq_instance, **correct_answer)
                else:
                    correct_answer['numbers'] = quiz_mcq_instance.total_numbers / len(
                        total_true_options) if correct_answer.get('correct_answer') else 0
                    McqsCorrectAnswer.objects.create(mcqs=quiz_mcq_instance, **correct_answer)

            # quiz_mcq_instance.total_numbers = total_numbers
            quiz_mcq_instance.save()

        for quiz_python in quiz_python_data:
            test_cases = quiz_python.pop('quizpythonproblemtestcase_set')
            quiz_python_problem_instance = QuizPythonProblem.objects.create(quiz=quiz, **quiz_python)
            for test_case in test_cases:
                QuizPythonProblemTestCase.objects.create(quiz_python_problem=quiz_python_problem_instance, **test_case)
        return quiz

    def update(self, instance, validated_data):
        quiz_mcqs_data = validated_data.pop('quizmcqs', [])
        quiz_python_data = validated_data.pop('quizpython', [])
        QuizMcqs.objects.filter(quiz=instance).delete()
        QuizPythonProblem.objects.filter(quiz=instance).delete()
        instance = super().update(instance, validated_data)
        for quiz_mcq_data in quiz_mcqs_data:
            # if quiz_mcq_data.get('quiz'):
            #     quiz = quiz_mcq_data.pop('quiz')
            # QuizMcqs.objects.create(quiz=instance, **quiz_mcq_data)

            if quiz_mcq_data.get('quiz'):
                quiz = quiz_mcq_data.pop('quiz')
            total_numbers = 0
            correct_answers = quiz_mcq_data.pop('mcqscorrectanswer_set')
            quiz_mcq_instance = QuizMcqs.objects.create(quiz=instance, **quiz_mcq_data)

            total_true_options = [sub['option' + str(index + 1)] for (index, sub) in enumerate(correct_answers) if
                                  sub['option' + str(index + 1)] == True]

            for correct_answer in correct_answers:
                if correct_answer.get('mcqs'):
                    mcqs = correct_answer.pop('mcqs')
                if correct_answer.pop('option1', False) or correct_answer.pop('option2', False) or correct_answer.pop(
                        'option3', False) or correct_answer.pop('option4', False):
                    correct_answer['numbers'] = quiz_mcq_instance.total_numbers / len(total_true_options)

                    McqsCorrectAnswer.objects.create(mcqs=quiz_mcq_instance, **correct_answer)
                else:
                    correct_answer['numbers'] = quiz_mcq_instance.total_numbers / len(
                        total_true_options) if correct_answer.get('correct_answer') else 0
                    McqsCorrectAnswer.objects.create(mcqs=quiz_mcq_instance, **correct_answer)

            # quiz_mcq_instance.total_numbers = total_numbers
            quiz_mcq_instance.save()

        for quiz_python in quiz_python_data:

            test_cases = quiz_python.pop('quizpythonproblemtestcase_set')
            if quiz_python.get('quiz'):
                quiz = quiz_python.pop('quiz')
            quiz_python_problem_instance = QuizPythonProblem.objects.create(quiz=instance, **quiz_python)

            for test_case in test_cases:

                if test_case.get('quiz_python_problem'):
                    quiz_python_problem = test_case.pop('quiz_python_problem')

                QuizPythonProblemTestCase.objects.create(quiz_python_problem=quiz_python_problem_instance, **test_case)
        return instance


class DeliveredMcqsAnswersSerializer(serializers.ModelSerializer):
    number = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = DeliveredMcqsAnswers
        fields = "__all__"


class DeliveredQuizMcqsSerializer(serializers.ModelSerializer):
    mcqs_answers = DeliveredMcqsAnswersSerializer(many=True, write_only=True)
    solved_mcqs_answers = DeliveredMcqsAnswersSerializer(many=True, read_only=True, source='deliveredmcqsanswers_set')
    mcqs_quiz_detail = QuizMcqsSerializer(read_only=True, source='mcqs_quiz')

    class Meta:
        model = DeliveredQuizMcqs
        fields = "__all__"


class DeliveredQuizPythonTestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveredQuizPythonTestCase
        fields = "__all__"


class DeliveredQuizPythonSerializer(serializers.ModelSerializer):
    test_cases = DeliveredQuizPythonTestCaseSerializer(many=True, write_only=True)
    python_quiz_detail = QuizPythonProblemSerializer(read_only=True, source='quiz_python_problem')

    class Meta:
        model = DeliveredQuizPython
        fields = "__all__"


class DeliveredQuizSerializer(serializers.ModelSerializer):
    deliveredquizmcqs = DeliveredQuizMcqsSerializer(many=True, write_only=True)
    deliveredquizpython = DeliveredQuizPythonSerializer(many=True, write_only=True)

    delivered_mcqs = DeliveredQuizMcqsSerializer(many=True, read_only=True, source='deliveredquizmcqs_set')
    delivered_python = DeliveredQuizPythonSerializer(many=True, read_only=True, source='deliveredquizpython_set')
    # course = CourseSerializer(many=True, read_only=True)
    quiz_detail = QuizSerializer(read_only=True, source='quiz')
    students_detail = UserSerializer(read_only=True, source='student')
    course_detail = CourseSerializer(read_only=True, source='course')

    course_average_marks_of_students = serializers.SerializerMethodField(read_only=True)
    course_total_marks_of_students = serializers.SerializerMethodField(read_only=True)
    course_average_marks = serializers.SerializerMethodField(read_only=True)
    student_average_marks = serializers.SerializerMethodField(read_only=True)
    student_total_marks = serializers.SerializerMethodField(read_only=True)

    def get_course_average_marks_of_students(self, obj):
        return obj.course_average_marks_of_students

    def get_course_total_marks_of_students(self, obj):
        return obj.course_total_marks_of_students

    def get_course_average_marks(self, obj):
        return obj.course_average_marks

    def get_student_average_marks(self, obj):
        return obj.student_average_marks

    def get_student_total_marks(self, obj):
        return obj.student_total_marks

    class Meta:
        model = DeliveredQuiz
        fields = "__all__"

    def create(self, validated_data):
        delivered_quiz_mcqs = validated_data.pop('deliveredquizmcqs')
        delivered_quiz_python = validated_data.pop('deliveredquizpython')
        quiz = DeliveredQuiz.objects.create(**validated_data)
        for quiz_mcq_data in delivered_quiz_mcqs:
            numbers = 0
            mcqs_answers = quiz_mcq_data.pop('mcqs_answers')
            delivered_mcqs_quiz_instance = DeliveredQuizMcqs.objects.create(delivered_quiz=quiz, **quiz_mcq_data)
            for mcqs in mcqs_answers:
                print(mcqs)
                if mcqs.get('is_correct_answer'):
                    numbers = numbers + mcqs.get('number')
                else:
                    numbers = numbers - mcqs.get('number')

                mcqs.pop('number')
                DeliveredMcqsAnswers.objects.create(delivered_mcqs_quiz=delivered_mcqs_quiz_instance, **mcqs)
            if len(mcqs_answers) > 1:
                delivered_mcqs_quiz_instance.numbers = numbers if numbers > 0 else 0
                delivered_mcqs_quiz_instance.save()

        for quiz_python_data in delivered_quiz_python:
            quiz_python_problem = quiz_python_data['quiz_python_problem']
            test_cases = quiz_python_data.pop('test_cases')
            # total_number = quiz_python_data.pop('total_number')
            if quiz_python_data.get('error'):
                quiz_python_data['numbers'] = 0
                quiz_python_data['is_compile_error'] = True
                DeliveredQuizPython.objects.create(delivered_quiz=quiz, **quiz_python_data)
            else:
                total_number = 0
                for test_case in test_cases:
                    total_number = total_number + test_case.get('numbers')
                quiz_python_data['numbers'] = total_number
                quiz_python_data['is_compile_error'] = False
                delivered_quiz_instance = DeliveredQuizPython.objects.create(delivered_quiz=quiz, **quiz_python_data)
                for test_case in test_cases:
                    DeliveredQuizPythonTestCase.objects.create(delivered_quiz=quiz, **test_case)

            # DeliveredQuizPython.objects.create(delivered_quiz=quiz, **quiz_python_data)
        total_number_mcqs = DeliveredQuizMcqs.objects.filter(delivered_quiz=quiz).aggregate(
            Sum("numbers"))
        total_number_python = DeliveredQuizPython.objects.filter(delivered_quiz=quiz).aggregate(
            Sum("numbers"))
        total_numbers = (total_number_mcqs.get('numbers__sum') if total_number_mcqs.get(
            'numbers__sum') else 0) + (total_number_python.get(
            'numbers__sum') if total_number_python.get(
            'numbers__sum') else 0)
        # quiz.total_numbers = total_number_mcqs.get('numbers__sum') if total_number_mcqs.get('numbers__sum') else 0
        quiz.total_numbers = total_numbers
        quiz.save()

        return quiz


class DeliveredQuizWriteOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveredQuiz
        fields = "__all__"
