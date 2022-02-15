# Generated by Django 2.2.9 on 2020-02-10 13:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("countries", "0001_initial"),
        ("documents", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Advice",
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
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("approve", "Approve"),
                            ("proviso", "Proviso"),
                            ("refuse", "Refuse"),
                            ("no_licence_required", "No Licence Required"),
                            ("not_applicable", "Not Applicable"),
                            ("conflicting", "Conflicting"),
                        ],
                        max_length=30,
                    ),
                ),
                ("text", models.TextField(blank=True, default=None, null=True)),
                ("note", models.TextField(blank=True, default=None, null=True)),
                ("proviso", models.TextField(blank=True, default=None, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Case",
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
                (
                    "reference_code",
                    models.CharField(default=None, editable=False, max_length=30, null=True, unique=True),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("application", "Application"),
                            ("goods_query", "Goods Query"),
                            ("end_user_advisory_query", "End User Advisory Query"),
                            ("hmrc_query", "HMRC Query"),
                            ("exhibition_clearance", "MOD Exhibition Clearance"),
                        ],
                        max_length=35,
                    ),
                ),
                ("submitted_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CaseAssignment",
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
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CaseDocument",
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
                    "type",
                    models.CharField(
                        choices=[("UPLOADED", "Uploaded"), ("GENERATED", "Generated")],
                        default="UPLOADED",
                        max_length=100,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("documents.document",),
        ),
        migrations.CreateModel(
            name="CaseNote",
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
                ("text", models.TextField(blank=True, default=None, max_length=2200, null=True)),
                ("is_visible_to_exporter", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CaseReferenceCode",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("reference_number", models.IntegerField()),
                ("year", models.IntegerField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name="CaseType",
            fields=[
                ("id", models.CharField(editable=False, max_length=30, primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("application", "Application"),
                            ("goods_query", "Goods Query"),
                            ("end_user_advisory_query", "End User Advisory Query"),
                            ("hmrc_query", "HMRC Query"),
                            ("exhibition_clearance", "MOD Exhibition Clearance"),
                        ],
                        max_length=35,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EcjuQuery",
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
                ("question", models.CharField(max_length=5000)),
                ("response", models.CharField(max_length=2200, null=True)),
                ("responded_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FinalAdvice",
            fields=[
                (
                    "advice_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="cases.Advice",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("cases.advice",),
        ),
        migrations.CreateModel(
            name="TeamAdvice",
            fields=[
                (
                    "advice_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="cases.Advice",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("cases.advice",),
        ),
        migrations.CreateModel(
            name="GoodCountryDecision",
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
                (
                    "decision",
                    models.CharField(
                        choices=[
                            ("approve", "Approve"),
                            ("proviso", "Proviso"),
                            ("refuse", "Refuse"),
                            ("no_licence_required", "No Licence Required"),
                            ("not_applicable", "Not Applicable"),
                            ("conflicting", "Conflicting"),
                        ],
                        max_length=30,
                    ),
                ),
                ("case", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="cases.Case")),
                ("country", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="countries.Country")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
