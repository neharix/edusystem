# Generated by Django 5.1.4 on 2025-02-26 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_diplomarequest_diplomareport_diplomarequestaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diplomarequest',
            name='previous_update_date',
        ),
        migrations.RemoveField(
            model_name='diplomarequest',
            name='update_date',
        ),
    ]
