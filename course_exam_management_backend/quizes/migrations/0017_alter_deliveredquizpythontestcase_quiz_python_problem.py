# Generated by Django 4.2 on 2023-04-27 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("quizes", "0016_deliveredquizpythontestcase"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deliveredquizpythontestcase",
            name="quiz_python_problem",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="quizes.quizpythonproblem",
            ),
        ),
    ]
