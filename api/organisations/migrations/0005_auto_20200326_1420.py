# Generated by Django 2.2.11 on 2020-03-26 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("organisations", "0004_auto_20200307_1805"),
    ]

    operations = [
        migrations.AlterField(
            model_name="site",
            name="address",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, related_name="site", to="addresses.Address"
            ),
        ),
        migrations.AlterModelTable(
            name="organisation",
            table="organisation",
        ),
        migrations.AlterModelTable(
            name="site",
            table="site",
        ),
    ]
