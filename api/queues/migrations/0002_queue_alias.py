# Generated by Django 3.1.14 on 2022-01-25 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("queues", "0001_squashed_0003_auto_20201210_1649"),
    ]

    operations = [
        migrations.AddField(
            model_name="queue",
            name="alias",
            field=models.TextField(default=None, null=True, unique=True, help_text="fixed static field for reference"),
        ),
    ]
