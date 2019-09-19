# Generated by Django 2.2.4 on 2019-09-19 10:37

from django.db import migrations, models
import django.db.models.deletion


def init(apps, schema_editor):

    Permission = apps.get_model('users', 'Permission')
    if not Permission.objects.filter(id='MANAGE_TEAM_ADVICE'):
        permission = Permission(id='MANAGE_TEAM_ADVICE',
                                name='Manage team advice')
        permission.save()

    if not Permission.objects.filter(id='MANAGE_FINAL_ADVICE'):
        permission = Permission(id='MANAGE_FINAL_ADVICE',
                                name='Manage final advice')
        permission.save()
        Permission.objects.get(id='MAKE_FINAL_DECISIONS').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        ('cases', '0002_auto_20190918_0838'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinalAdvice',
            fields=[
                ('advice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cases.Advice')),
            ],
            bases=('cases.advice',),
        ),
        migrations.AlterField(
            model_name='advice',
            name='type',
            field=models.CharField(choices=[('approve', 'Approve'), ('proviso', 'Proviso'), ('refuse', 'Refuse'), ('no_licence_required', 'No Licence Required'), ('not_applicable', 'Not Applicable'), ('conflicting', 'Conflicting')], max_length=30),
        ),
        migrations.CreateModel(
            name='TeamAdvice',
            fields=[
                ('advice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cases.Advice')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.Team')),
            ],
            bases=('cases.advice',),
        ),
        migrations.RunPython(init),
    ]
