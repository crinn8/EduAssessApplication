# Generated by Django 4.2 on 2023-04-08 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="image",
            field=models.ImageField(null=True, upload_to="courses/"),
        ),
    ]