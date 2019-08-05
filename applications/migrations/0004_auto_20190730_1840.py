# Generated by Django 2.2.3 on 2019-07-30 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_application_ultimate_end_users'),
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='application_status', to='statuses.CaseStatus'),
        ),
    ]
