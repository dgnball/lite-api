# Generated by Django 2.2.8 on 2020-01-23 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0006_auto_20200121_1411"),
    ]

    operations = [
        migrations.AlterModelOptions(name="goodonapplication", options={"ordering": ["created_at"]},),
    ]
