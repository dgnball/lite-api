# Generated by Django 2.2.16 on 2021-01-21 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parties", "0010_auto_20200722_1339"),
    ]

    operations = [
        migrations.AddField(model_name="party", name="signatory_name_euu", field=models.TextField(blank=True),),
    ]
