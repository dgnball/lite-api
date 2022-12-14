# Generated by Django 3.2.16 on 2022-12-14 10:20

from django.db import migrations


def update_nsg_regimes(apps, schema_editor):
    # The original csv files to import the NSG regimes in 0008_add_nsg_regimes
    # have been updated and fixed so that they correspond to the correct
    # regimes, however this will have been run on environments already so this
    # migration is here to tidy up the previously incorrect migration
    RegimeSubsection = apps.get_model("regimes", "RegimeSubsection")
    RegimeEntry = apps.get_model("regimes", "RegimeEntry")

    currently_trigger_list = list(
        RegimeEntry.objects.filter(subsection__name="NSG Potential Trigger List", name__istartswith="N").values_list(
            "pk", flat=True
        )
    )

    currently_dual_use = list(
        RegimeEntry.objects.filter(
            subsection__name="NSG Dual-Use",
            name__istartswith="T",
        ).values_list("pk", flat=True)
    )

    trigger_list_subsection = RegimeSubsection.objects.get(name="NSG Potential Trigger List")
    RegimeEntry.objects.filter(pk__in=currently_dual_use).update(subsection=trigger_list_subsection)

    dual_use_subsection = RegimeSubsection.objects.get(name="NSG Dual-Use")
    RegimeEntry.objects.filter(pk__in=currently_trigger_list).update(subsection=dual_use_subsection)


class Migration(migrations.Migration):

    dependencies = [
        ("regimes", "0008_add_nsg_regimes"),
    ]

    operations = [
        migrations.RunPython(
            update_nsg_regimes,
            migrations.RunPython.noop,
        ),
    ]
