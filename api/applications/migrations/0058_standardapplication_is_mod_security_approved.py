# Generated by Django 3.2.15 on 2022-09-13 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0057_alter_goodonapplication_unit"),
    ]

    operations = [
        migrations.AddField(
            model_name="standardapplication",
            name="is_mod_security_approved",
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
