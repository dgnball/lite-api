# Generated by Django 2.2.13 on 2020-06-11 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_auto_20200603_1252"),
        ("cases", "0033_auto_20200610_1612"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ComplianceCase",
        ),
    ]
