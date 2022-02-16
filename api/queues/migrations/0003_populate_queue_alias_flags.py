# Generated by Django 3.2.11 on 2022-01-27 09:48

from django.db import migrations


def populate_queue_alias_flags(apps, schema_editor):
    flags = {
        "f458094c-1fed-4222-ac70-ff5fa20ff649": "FCDO_CASES_TO_REVIEW",
        "5e772575-9ae4-4a16-b55b-7e1476d810c4": "FCDO_COUNTER_SIGNING",
        "a4c5bd9d-0d06-4856-abe1-c71d73abe636": "MOD_CASES_TO_REVIEW",
        "0dd6c6f0-8f8b-4c03-b68f-0d8b04225369": "MOD_DI_CASES_TO_REVIEW",
        "a84d6556-782e-4002-abe2-8bc1e5c2b162": "MOD_DSR_CASES_TO_REVIEW",
        "1a5f47ee-ef5e-456b-914c-4fa629b4559c": "MOD_DSTL_CASES_TO_REVIEW",
        "93d1bc19-979d-4ba3-a57c-b0ce253c6237": "MOD_WECA_CASES_TO_REVIEW",
        "f0e7c2fa-100f-42ad-b740-bb072393e664": "LU_POST_CIRC_FINALISE",
    }
    Queue = apps.get_model("queues", "Queue")
    for f in flags.keys():
        team = Queue.objects.filter(id=f)
        if team.exists():
            team.update(alias=flags[f])


class Migration(migrations.Migration):

    dependencies = [
        ("queues", "0002_queue_alias"),
    ]

    operations = [
        migrations.RunPython(populate_queue_alias_flags, migrations.RunPython.noop),
    ]
