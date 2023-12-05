from django.db import models
from django.db.models import Avg, Sum
from users.models import User


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class QuizMcqs(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    question = models.TextField()
    option1 = models.CharField(max_length=255, null=True, blank=True)
    option2 = models.CharField(max_length=255, null=True, blank=True)
    option3 = models.CharField(max_length=255, null=True, blank=True)
    option4 = models.CharField(max_length=255, null=True, blank=True)
    total_numbers = models.FloatField()


class McqsCorrectAnswer(models.Model):
    mcqs = models.ForeignKey(QuizMcqs, on_delete=models.CASCADE, null=True)
    numbers = models.FloatField()
    correct_answer = models.CharField(max_length=255, null=True, blank=True)


class QuizPythonProblem(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    question = models.TextField()
    numbers = models.FloatField(null=True)
    correct_answer = models.CharField(max_length=255, null=True, blank=True)
    sample_code = models.TextField(null=True)


class QuizPythonProblemTestCase(models.Model):
    quiz_python_problem = models.ForeignKey(QuizPythonProblem, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)
    text = models.CharField(max_length=255)
    numbers = models.FloatField()
    correct_answer = models.CharField(max_length=255)


class DeliveredQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=False)
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    total_numbers = models.FloatField(null=True, blank=True)
    is_custom_add = models.BooleanField(default=False)

    @property
    def course_average_marks_of_students(self):
        return DeliveredQuiz.objects.filter(course_id=self.course, student_id=self.student).aggregate(
            Avg('total_numbers'))

    @property
    def course_total_marks_of_students(self):
        return DeliveredQuiz.objects.filter(course_id=self.course, student_id=self.student).aggregate(
            Sum('total_numbers'))

    @property
    def course_average_marks(self):
        return DeliveredQuiz.objects.filter(course_id=self.course).aggregate(
            Avg('total_numbers'))

    @property
    def student_average_marks(self):
        return DeliveredQuiz.objects.filter(student_id=self.student).aggregate(
            Avg('total_numbers'))

    @property
    def student_total_marks(self):
        return DeliveredQuiz.objects.filter(student_id=self.student).aggregate(
            Sum('total_numbers'))


class DeliveredQuizMcqs(models.Model):
    delivered_quiz = models.ForeignKey(DeliveredQuiz, on_delete=models.CASCADE, null=True)
    mcqs_quiz = models.ForeignKey(QuizMcqs, on_delete=models.CASCADE)
    numbers = models.FloatField()


class DeliveredMcqsAnswers(models.Model):
    delivered_mcqs_quiz = models.ForeignKey(DeliveredQuizMcqs, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=255)
    is_correct_answer = models.BooleanField(max_length=255)


class DeliveredQuizPython(models.Model):
    delivered_quiz = models.ForeignKey(DeliveredQuiz, on_delete=models.CASCADE, null=True)
    quiz_python_problem = models.ForeignKey(QuizPythonProblem, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, null=True, blank=True)
    code = models.TextField(null=True, blank=True)
    is_correct_answer = models.BooleanField(default=False)
    is_compile_error = models.BooleanField(default=False)
    numbers = models.FloatField(null=True)
    error = models.CharField(max_length=255, null=True)


class DeliveredQuizPythonTestCase(models.Model):
    delivered_quiz = models.ForeignKey(DeliveredQuiz, on_delete=models.CASCADE, null=True)
    quiz_python_problem = models.ForeignKey(QuizPythonProblem, on_delete=models.CASCADE, null=True)
    test_case = models.ForeignKey(QuizPythonProblemTestCase, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, null=True)
    is_correct_answer = models.BooleanField(default=False)
    numbers = models.FloatField(null=True)
