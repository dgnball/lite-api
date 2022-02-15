# Generated by Django 2.2.9 on 2020-02-10 13:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("flags", "0001_initial"),
        ("countries", "0001_initial"),
        ("documents", "0001_initial"),
        (
            "applications",
            "0002_baseapplication_countryonapplication_exhibitionclearanceapplication_externallocationonapplication_go",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="GoodsType",
            fields=[
                (
                    "created_at",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created_at"
                    ),
                ),
                (
                    "updated_at",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="updated_at"
                    ),
                ),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("description", models.TextField(blank=True, default=None, max_length=2000, null=True)),
                ("is_good_controlled", models.BooleanField(blank=True, default=None, null=True)),
                ("control_code", models.TextField(blank=True, default=None, null=True)),
                ("is_good_incorporated", models.BooleanField(blank=True, default=None, null=True)),
                ("comment", models.TextField(blank=True, default=None, null=True)),
                ("report_summary", models.TextField(blank=True, default=None, null=True)),
                (
                    "application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="base_application",
                        to="applications.BaseApplication",
                    ),
                ),
                ("countries", models.ManyToManyField(default=[], related_name="goods_type", to="countries.Country")),
                ("flags", models.ManyToManyField(related_name="goods_type", to="flags.Flag")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="GoodsTypeDocument",
            fields=[
                (
                    "document_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="documents.Document",
                    ),
                ),
                ("description", models.TextField(blank=True, default=None, max_length=280, null=True)),
                (
                    "goods_type",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="goodstype.GoodsType"),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("documents.document",),
        ),
    ]
