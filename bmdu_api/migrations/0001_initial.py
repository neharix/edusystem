# Generated by Django 5.2.1 on 2025-07-04 18:54

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnualUpdateReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Classificator',
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
            name='Degree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('duration', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)])),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('abbreviation', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('is_visible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExpulsionReason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('abbreviation', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
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
            name='DiplomaRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('simple_diploma_count', models.PositiveIntegerField(default=0)),
                ('honor_diploma_count', models.PositiveIntegerField(default=0)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('verdict_date', models.DateTimeField(blank=True, null=True)),
                ('verdict', models.CharField(blank=True, choices=[('C', 'Confirmed'), ('R', 'Rejected')], max_length=1, null=True)),
                ('allowed_until', models.DateTimeField(blank=True, null=True)),
                ('is_obsolete', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='diploma_request_sender', to=settings.AUTH_USER_MODEL)),
                ('viewed_by', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DiplomaReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('two_year_work_off', models.PositiveIntegerField(default=0)),
                ('died', models.PositiveIntegerField(default=0)),
                ('went_abroad', models.PositiveIntegerField(default=0)),
                ('other_reasons', models.PositiveIntegerField(default=0)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('verdict_date', models.DateTimeField(blank=True, null=True)),
                ('verdict', models.CharField(blank=True, choices=[('C', 'Confirmed')], max_length=1, null=True)),
                ('diploma_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bmdu_api.diplomarequest')),
            ],
            options={
                'ordering': ['-verdict_date'],
            },
        ),
        migrations.CreateModel(
            name='DiplomaRequestAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_simple_to', models.PositiveIntegerField(default=0)),
                ('update_honor_to', models.PositiveIntegerField(default=0)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('verdict_date', models.DateTimeField(blank=True, null=True)),
                ('verdict', models.CharField(blank=True, choices=[('C', 'Confirmed')], max_length=1, null=True)),
                ('diploma_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bmdu_api.diplomarequest')),
            ],
            options={
                'ordering': ['-verdict_date'],
            },
        ),
        migrations.CreateModel(
            name='HighSchool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('abbreviation', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('lat', models.FloatField(blank=True, default=37.95)),
                ('lng', models.FloatField(blank=True, default=58.38)),
                ('is_complex_branched', models.BooleanField(default=False)),
                ('manager', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.profile')),
            ],
        ),
        migrations.CreateModel(
            name='HighSchoolFaculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bmdu_api.faculty')),
                ('high_school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bmdu_api.highschool')),
            ],
        ),
        migrations.CreateModel(
            name='FacultyDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_visible', models.BooleanField(default=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bmdu_api.department')),
                ('high_school_faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bmdu_api.highschoolfaculty')),
            ],
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('abbreviation', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('classificator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bmdu_api.classificator')),
                ('degree', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bmdu_api.degree')),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentSpecialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identification_status', models.CharField(choices=[('P', 'Bölek'), ('CS', 'Umumylaşdyrlan'), ('D', 'Ýönekeý')], default='D', max_length=2)),
                ('shell_name', models.CharField(blank=True, max_length=500, null=True)),
                ('parts', models.ManyToManyField(blank=True, to='bmdu_api.departmentspecialization')),
                ('faculty_department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bmdu_api.facultydepartment')),
                ('specialization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bmdu_api.specialization')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=400)),
                ('gender', models.CharField(choices=[('M', 'Oglan'), ('F', 'Gyz')], max_length=1)),
                ('family_status', models.CharField(choices=[('FR', 'Hossarly'), ('HO', 'Ýarym ýetim'), ('CO', 'Doly ýetim'), ('OE', 'Ýetimler öýünde ösen')], max_length=2)),
                ('payment_type', models.CharField(choices=[('P', 'Tölegli'), ('B', 'Býudjet')], max_length=1)),
                ('birth_date', models.DateField(default=datetime.date(1970, 1, 1))),
                ('admission_date', models.DateField()),
                ('registered_place', models.TextField()),
                ('study_year', models.CharField(default='1', max_length=3)),
                ('phone_number', models.CharField(max_length=500)),
                ('passport', models.CharField(max_length=500)),
                ('military_service', models.CharField(blank=True, max_length=500, null=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('is_expelled', models.BooleanField(default=False)),
                ('is_obsolete', models.BooleanField(default=False)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bmdu_api.country')),
                ('high_school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bmdu_api.highschool')),
                ('nationality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bmdu_api.nationality')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bmdu_api.region')),
                ('specialization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bmdu_api.departmentspecialization')),
            ],
        ),
        migrations.CreateModel(
            name='ReinstateRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField()),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('verdict_date', models.DateTimeField(blank=True, null=True)),
                ('verdict', models.CharField(blank=True, choices=[('C', 'Confirmed'), ('R', 'Rejected')], max_length=1, null=True)),
                ('is_obsolete', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reinstate_request_sender', to=settings.AUTH_USER_MODEL)),
                ('viewed_by', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bmdu_api.student')),
            ],
            options={
                'ordering': ['verdict_date'],
            },
        ),
        migrations.CreateModel(
            name='ExpulsionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField()),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('verdict_date', models.DateTimeField(blank=True, null=True)),
                ('verdict', models.CharField(blank=True, choices=[('C', 'Confirmed'), ('R', 'Rejected')], max_length=1, null=True)),
                ('is_obsolete', models.BooleanField(default=False)),
                ('reason', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bmdu_api.expulsionreason')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expulsion_request_sender', to=settings.AUTH_USER_MODEL)),
                ('viewed_by', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bmdu_api.student')),
            ],
            options={
                'ordering': ['verdict_date'],
            },
        ),
        migrations.CreateModel(
            name='TeacherStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workload_1_25', models.PositiveIntegerField(default=0)),
                ('workload_1_00', models.PositiveIntegerField(default=0)),
                ('workload_0_75', models.PositiveIntegerField(default=0)),
                ('workload_0_50', models.PositiveIntegerField(default=0)),
                ('doctor_degree', models.PositiveIntegerField(default=0)),
                ('candidate_degree', models.PositiveIntegerField(default=0)),
                ('professor', models.PositiveIntegerField(default=0)),
                ('docent', models.PositiveIntegerField(default=0)),
                ('department_head', models.PositiveIntegerField(default=0)),
                ('professor_job', models.PositiveIntegerField(default=0)),
                ('docent_job', models.PositiveIntegerField(default=0)),
                ('senior_teachers', models.PositiveIntegerField(default=0)),
                ('teachers', models.PositiveIntegerField(default=0)),
                ('intern_teachers', models.PositiveIntegerField(default=0)),
                ('allowed_until', models.DateTimeField(blank=True, null=True)),
                ('is_obsolete', models.BooleanField(default=False)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('verdict_date', models.DateTimeField(blank=True, null=True)),
                ('verdict', models.CharField(blank=True, choices=[('C', 'Confirmed'), ('R', 'Rejected')], max_length=1, null=True)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher_statement_sender', to=settings.AUTH_USER_MODEL)),
                ('viewed_by', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
