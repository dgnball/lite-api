# Generated by Django 2.2.17 on 2021-01-19 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("external_data", "0006_auto_20210118_1124"),
    ]

    operations = [
        migrations.AddField(
            model_name="denial",
            name="end_use",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]
