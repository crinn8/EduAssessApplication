# Generated by Django 4.2 on 2023-04-28 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quizes", "0017_alter_deliveredquizpythontestcase_quiz_python_problem"),
    ]

    operations = [
        migrations.AddField(
            model_name="deliveredquizpython",
            name="error",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="deliveredquizpython",
            name="code",
            field=models.TextField(blank=True, null=True),
        ),
    ]
