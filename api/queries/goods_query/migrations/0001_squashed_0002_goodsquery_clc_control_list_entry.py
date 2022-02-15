# Generated by Django 3.1.8 on 2021-04-26 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [("goods_query", "0001_initial"), ("goods_query", "0002_goodsquery_clc_control_list_entry")]

    initial = True

    dependencies = [
        ("goods", "0001_initial"),
        ("queries", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GoodsQuery",
            fields=[
                (
                    "query_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="queries.query",
                    ),
                ),
                ("clc_raised_reasons", models.TextField(blank=True, default=None, max_length=2000, null=True)),
                ("pv_grading_raised_reasons", models.TextField(blank=True, default=None, max_length=2000, null=True)),
                ("clc_responded", models.BooleanField(default=None, null=True)),
                ("pv_grading_responded", models.BooleanField(default=None, null=True)),
                (
                    "good",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, related_name="good", to="goods.good"
                    ),
                ),
                ("clc_control_list_entry", models.TextField(blank=True, default=None, max_length=200, null=True)),
            ],
            options={
                "abstract": False,
            },
            bases=("queries.query",),
        ),
    ]
