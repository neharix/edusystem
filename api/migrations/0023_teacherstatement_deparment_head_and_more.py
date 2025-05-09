# Generated by Django 5.1.4 on 2025-03-01 17:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_alter_diplomarequest_allowed_until_teacherstatement'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherstatement',
            name='deparment_head',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teacherstatement',
            name='docent',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teacherstatement',
            name='docent_job',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teacherstatement',
            name='intern_teachers',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teacherstatement',
            name='professor',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teacherstatement',
            name='professor_job',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teacherstatement',
            name='senior_teachers',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teacherstatement',
            name='teachers',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='diplomarequest',
            name='allowed_until',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 31, 17, 50, 26, 731352, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='teacherstatement',
            name='allowed_until',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 31, 17, 50, 26, 733005, tzinfo=datetime.timezone.utc)),
        ),
    ]
