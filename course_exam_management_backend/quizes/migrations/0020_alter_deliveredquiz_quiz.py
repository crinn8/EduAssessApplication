# Generated by Django 4.2 on 2023-05-04 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("quizes", "0019_deliveredquiz_is_custom_add"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deliveredquiz",
            name="quiz",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="quizes.quiz"
            ),
        ),
    ]
