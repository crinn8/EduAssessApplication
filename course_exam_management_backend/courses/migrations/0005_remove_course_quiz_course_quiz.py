# Generated by Django 4.2 on 2023-04-23 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quizes", "0011_alter_deliveredquizpython_numbers"),
        ("courses", "0004_course_quiz"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="quiz",
        ),
        migrations.AddField(
            model_name="course",
            name="quiz",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="courses", to="quizes.quiz"
            ),
        ),
    ]
