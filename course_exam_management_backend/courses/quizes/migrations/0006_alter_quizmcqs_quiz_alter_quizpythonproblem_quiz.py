# Generated by Django 4.2 on 2023-04-20 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("quizes", "0005_alter_quizmcqs_question_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quizmcqs",
            name="quiz",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="quizes.quiz"
            ),
        ),
        migrations.AlterField(
            model_name="quizpythonproblem",
            name="quiz",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="quizes.quiz"
            ),
        ),
    ]