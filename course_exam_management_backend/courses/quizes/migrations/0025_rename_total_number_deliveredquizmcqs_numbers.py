# Generated by Django 4.2 on 2023-05-14 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("quizes", "0024_rename_numbers_deliveredquizmcqs_total_number_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="deliveredquizmcqs",
            old_name="total_number",
            new_name="numbers",
        ),
    ]