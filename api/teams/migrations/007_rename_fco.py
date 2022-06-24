# Generated by Django 3.2.11 on 2022-06-24 09:47

from django.db import migrations


def rename_fco(apps, schema_editor):
    Department = apps.get_model("departments", "Department")
    fco = Department.objects.filter(name="FCO")
    if fco.exists():
        fco.update(name="FCDO")


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0007_auto_20220531_1344"),
    ]

    operations = [
        migrations.RunPython(rename_fco, migrations.RunPython.noop),
    ]
