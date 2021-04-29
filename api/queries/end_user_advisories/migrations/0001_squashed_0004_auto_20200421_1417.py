# Generated by Django 3.1.8 on 2021-04-26 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('end_user_advisories', '0001_initial'), ('end_user_advisories', '0002_enduseradvisoryquery_end_user'), ('end_user_advisories', '0003_remove_enduseradvisoryquery_copy_of'), ('end_user_advisories', '0004_auto_20200421_1417')]

    initial = True

    dependencies = [
        ('queries', '0001_initial'),
        ('parties', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EndUserAdvisoryQuery',
            fields=[
                ('query_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='queries.query')),
                ('note', models.TextField(blank=True, default=None, null=True)),
                ('reasoning', models.TextField(blank=True, default=None, null=True)),
                ('nature_of_business', models.TextField(blank=True, default=None, null=True)),
                ('contact_name', models.TextField(blank=True, default=None, null=True)),
                ('contact_email', models.EmailField(blank=True, default=None, max_length=254)),
                ('contact_job_title', models.TextField(blank=True, default=None, null=True)),
                ('contact_telephone', models.CharField(default=None, max_length=15)),
                ('end_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='eua_query', to='parties.party')),
            ],
            options={
                'abstract': False,
                'ordering': ['created_at'],
            },
            bases=('queries.query',),
        ),
    ]
