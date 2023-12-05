# Generated by Django 4.2 on 2023-04-27 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("quizes", "0015_alter_quizpythonproblem_correct_answer"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeliveredQuizPythonTestCase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("answer", models.CharField(max_length=255, null=True)),
                ("is_correct_answer", models.BooleanField(default=False)),
                ("numbers", models.FloatField(null=True)),
                (
                    "delivered_quiz",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="quizes.deliveredquiz",
                    ),
                ),
                (
                    "quiz_python_problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="quizes.quizpythonproblem",
                    ),
                ),
                (
                    "test_case",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="quizes.quizpythonproblemtestcase",
                    ),
                ),
            ],
        ),
    ]