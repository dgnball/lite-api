# Generated by Django 2.2 on 2019-05-21 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0003_add_sites_no_constraint'),
        ('drafts', '0006_sitesondraft'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SitesOnDraft',
            new_name='SiteOnDraft',
        ),
    ]
