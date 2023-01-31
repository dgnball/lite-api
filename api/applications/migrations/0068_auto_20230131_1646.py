# Generated by Django 3.2.16 on 2023-01-31 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("report_summaries", "0005_update_picklist_casing"),
        ("applications", "0067_auto_20230126_1033"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goodonapplication",
            name="report_summary_prefix",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="report_summary_prefix_goa",
                to="report_summaries.reportsummaryprefix",
            ),
        ),
        migrations.AlterField(
            model_name="goodonapplication",
            name="report_summary_subject",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="report_summary_subject_goa",
                to="report_summaries.reportsummarysubject",
            ),
        ),
    ]
