# Generated by Django 5.2.1 on 2025-07-04 18:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.TextField(blank=True, null=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.profile')),
            ],
        ),
        migrations.CreateModel(
            name='EducationCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('phone_number', models.CharField(max_length=150)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lng', models.FloatField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('buildings_count', models.PositiveIntegerField(default=0)),
                ('rooms_count', models.PositiveIntegerField(default=0)),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('books_count', models.PositiveIntegerField(default=0)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mmu_api.country')),
                ('workers', models.ManyToManyField(blank=True, to='main.profile')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('content', models.FileField(upload_to='mmu/')),
                ('is_active', models.BooleanField(default=True)),
                ('to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_to', to='main.profile')),
                ('to_storage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mmu_api.educationcenter')),
                ('uploader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.profile')),
            ],
        ),
        migrations.AddField(
            model_name='educationcenter',
            name='accreditation_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accredition_file', to='mmu_api.file'),
        ),
        migrations.AddField(
            model_name='educationcenter',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mmu_api.region'),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=500)),
                ('place_of_residence', models.TextField()),
                ('phone_number', models.CharField(max_length=100)),
                ('education_degree', models.CharField(choices=[('high', 'High'), ('incompleteHigh', 'Incomplete High'), ('secondary', 'Secondary'), ('specialSecondary', 'Special Secondary')], max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mmu_api.country')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mmu_api.region')),
                ('specializations', models.ManyToManyField(to='mmu_api.specialization')),
            ],
        ),
        migrations.AddField(
            model_name='educationcenter',
            name='staff',
            field=models.ManyToManyField(blank=True, to='mmu_api.staff'),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=500)),
                ('place_of_residence', models.TextField()),
                ('phone_number', models.CharField(max_length=250)),
                ('study_or_working_place', models.TextField()),
                ('achievements', models.ManyToManyField(blank=True, to='mmu_api.achievement')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mmu_student_country', to='mmu_api.country')),
                ('nationality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mmu_student_nationality', to='mmu_api.nationality')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mmu_student_region', to='mmu_api.region')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('hours', models.PositiveIntegerField(default=0)),
                ('date_start', models.DateField(blank=True, null=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('lesson_time_start', models.TimeField(blank=True, null=True)),
                ('lesson_time_end', models.TimeField(blank=True, null=True)),
                ('direction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mmu_api.direction')),
                ('education_center', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mmu_api.educationcenter')),
                ('students', models.ManyToManyField(to='mmu_api.student')),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.PositiveIntegerField(default=0)),
                ('temp_key', models.CharField(max_length=20)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mmu_api.course')),
                ('education_center', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mmu_api.educationcenter')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mmu_api.student')),
            ],
        ),
    ]
