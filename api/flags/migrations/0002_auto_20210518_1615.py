# Generated by Django 3.1.8 on 2021-05-18 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("flags", "0001_squashed_0012_auto_20210309_1521"),
    ]

    operations = [
        migrations.RenameField(
            model_name="flag",
            old_name="blocks_approval",
            new_name="blocks_finalising",
        ),
    ]
