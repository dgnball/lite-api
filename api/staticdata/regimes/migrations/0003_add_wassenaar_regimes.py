# Generated by Django 3.2.15 on 2022-09-26 11:48

from django.db import migrations, transaction


from api.staticdata.regimes.enums import RegimesEnum, RegimeSubsectionsEnum


def create_wassenaar_regimes(apps, schema_editor):
    Regime = apps.get_model("regimes", "Regime")
    RegimeSubsection = apps.get_model("regimes", "RegimeSubsection")
    RegimeEntry = apps.get_model("regimes", "RegimeEntry")

    with transaction.atomic():
        wassenaar_regime = Regime.objects.create(
            id=RegimesEnum.WASSENAAR,
            name="WASSENAAR",
        )

        # We have a data model for the regimes that always has three levels in the hierarchy.
        # In the case of Wassenaar there isn't really a subsection but to be consistent with the hierarchy of models
        # we create dummy entries inbetween.
        for pk, name in [
            (
                RegimeSubsectionsEnum.WASSENAAR_ARRANGEMENT,
                "Wassenaar Arrangement",
            ),
            (
                RegimeSubsectionsEnum.WASSENAAR_ARRANGEMENT_SENSITIVE,
                "Wassenaar Arrangement Sensitive",
            ),
            (
                RegimeSubsectionsEnum.WASSENAAR_ARRANGEMENT_VERY_SENSITIVE,
                "Wassenaar Arrangement Very Sensitive",
            ),
        ]:
            subsection = RegimeSubsection.objects.create(
                id=pk,
                name=name,
                regime=wassenaar_regime,
            )
            RegimeEntry.objects.create(
                name=name,
                subsection=subsection,
            )


class Migration(migrations.Migration):

    dependencies = [
        ("regimes", "0002_add_mtcr_regimes"),
    ]

    operations = [
        migrations.RunPython(
            create_wassenaar_regimes,
            migrations.RunPython.noop,
        ),
    ]
