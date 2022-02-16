# Generated by Django 2.2.10 on 2020-03-04 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0009_f680clearanceapplication_types"),
    ]

    operations = [
        migrations.AddField(
            model_name="exhibitionclearanceapplication",
            name="first_exhibition_date",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="exhibitionclearanceapplication",
            name="reason_for_clearance",
            field=models.TextField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="exhibitionclearanceapplication",
            name="required_by_date",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="exhibitionclearanceapplication",
            name="title",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="goodonapplication",
            name="item_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("equipment", "Equipment"),
                    ("model", "Model"),
                    ("datasheet", "Datasheet"),
                    ("brochure", "Brochure"),
                    ("video", "Video"),
                    ("other", "Other"),
                ],
                default=None,
                max_length=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="goodonapplication",
            name="other_item_type",
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="goodonapplication",
            name="is_good_incorporated",
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="goodonapplication",
            name="unit",
            field=models.CharField(
                blank=True,
                choices=[
                    ("GRM", "Gram(s)"),
                    ("KGM", "Kilogram(s)"),
                    ("NAR", "Number of articles"),
                    ("MTK", "Square metre(s)"),
                    ("MTR", "Metre(s)"),
                    ("LTR", "Litre(s)"),
                    ("MTQ", "Cubic metre(s)"),
                ],
                default=None,
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="goodonapplication",
            name="value",
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=256, null=True),
        ),
    ]
