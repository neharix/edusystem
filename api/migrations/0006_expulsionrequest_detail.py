# Generated by Django 5.1.4 on 2025-02-22 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_expulsionrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='expulsionrequest',
            name='detail',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
