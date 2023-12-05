# Generated by Django 4.2 on 2023-04-27 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quizes", "0013_quizpythonproblemtestcase_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quizpythonproblem",
            name="correct_answer",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="quizpythonproblem",
            name="numbers",
            field=models.FloatField(null=True),
        ),
    ]
