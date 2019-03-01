# Generated by Django 2.1.3 on 2019-03-01 15:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Draft',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.TextField(default=None)),
                ('control_code', models.TextField(blank=True, default=None, null=True)),
                ('activity', models.TextField(blank=True, default=None, null=True)),
                ('destination', models.TextField(blank=True, default=None, null=True)),
                ('usage', models.TextField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'draft',
            },
        ),
    ]
