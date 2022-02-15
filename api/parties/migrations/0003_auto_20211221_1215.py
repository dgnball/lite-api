# Generated by Django 3.1.8 on 2021-12-21 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parties", "0002_remove_name_length_limit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="party",
            name="type",
            field=models.CharField(
                choices=[
                    ("consignee", "Consignee"),
                    ("end_user", "End-user"),
                    ("ultimate_end_user", "Ultimate end user"),
                    ("third_party", "Third party"),
                    ("additional_contact", "Additional contact"),
                ],
                max_length=20,
            ),
        ),
    ]
