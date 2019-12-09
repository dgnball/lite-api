# Generated by Django 2.2.4 on 2019-12-09 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("queries", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ControlListClassificationQuery",
            fields=[
                (
                    "query_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="queries.Query",
                    ),
                ),
                ("details", models.TextField(blank=True, default=None, null=True)),
            ],
            options={"abstract": False,},
            bases=("queries.query",),
        ),
    ]
