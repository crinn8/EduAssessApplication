# Generated by Django 4.2 on 2023-06-02 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quizes", "0025_rename_total_number_deliveredquizmcqs_numbers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deliveredquizpython",
            name="answer",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
