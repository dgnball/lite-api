# Generated by Django 2.2.11 on 2020-03-20 12:55

from django.db import migrations


def convert_users(apps, schema_editor):
    CaseAssignment = apps.get_model("cases", "CaseAssignment")
    case_assignments = CaseAssignment.objects.all()
    for assignment in case_assignments:
        for user in assignment.users.all():
            CaseAssignment.objects.create(case=assignment.case, queue=assignment.queue, user=user)
        assignment.delete()


def reverse_users(apps, schema_editor):
    Case = apps.get_model("cases", "Case")
    Queue = apps.get_model("queues", "Queue")
    CaseAssignment = apps.get_model("cases", "CaseAssignment")
    cases = Case.objects.all()
    queues = Queue.objects.all()

    for case in cases:
        for queue in queues:
            assignments = CaseAssignment.objects.filter(case=case, queue=queue)
            users = [assignment.user for assignment in assignments]
            assignment = CaseAssignment.objects.create(case=case, queue=queue)
            assignment.users.set(users)
            assignments.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0009_auto_20200320_1210"),
    ]

    operations = [
        migrations.RunPython(convert_users, reverse_code=reverse_users),
    ]
