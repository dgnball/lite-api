# Generated by Django 3.2.16 on 2022-11-25 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="safe",
            field=models.BooleanField(null=True),
        ),
    ]
