# Generated by Django 3.1.7 on 2021-03-01 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0012_flag_removable_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flag',
            name='name',
            field=models.CharField(default='Untitled Flag', max_length=100, unique=True),
        ),
    ]
