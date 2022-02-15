# Generated by Django 3.1.8 on 2021-04-26 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [
        ("generated_documents", "0001_initial"),
        ("generated_documents", "0002_generatedcasedocument_template"),
        ("generated_documents", "0003_auto_20200218_1203"),
        ("generated_documents", "0004_auto_20200311_1124"),
        ("generated_documents", "0005_generatedcasedocument_advice_type"),
        ("generated_documents", "0006_generatedcasedocument_licence"),
    ]

    initial = True

    dependencies = [
        ("cases", "0004_auto_20200211_1459"),
        ("letter_templates", "0001_initial"),
        ("licences", "0006_licence_sent_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="GeneratedCaseDocument",
            fields=[
                (
                    "casedocument_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="cases.casedocument",
                    ),
                ),
                ("text", models.TextField(blank=True)),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="letter_templates.lettertemplate"
                    ),
                ),
                (
                    "advice_type",
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
                        null=True,
                    ),
                ),
                (
                    "licence",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="licences.licence"),
                ),
            ],
            options={
                "abstract": False,
                "ordering": ["name"],
            },
            bases=("cases.casedocument",),
        ),
    ]
