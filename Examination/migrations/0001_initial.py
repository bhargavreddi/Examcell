# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-03-12 05:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arrangement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('set_number', models.IntegerField()),
                ('malpractice', models.BooleanField()),
                ('blankomr', models.BooleanField()),
                ('attendance', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('classroom_number', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ClassroomCapacity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField(default=24)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Examination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examination_name', models.CharField(max_length=225)),
                ('type', models.CharField(max_length=30)),
                ('month', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ExaminationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('faculty_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('faculty_name', models.CharField(max_length=225)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Invigilation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Classroom')),
                ('examination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Examination')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='InvigilationCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remaining', models.IntegerField(default=0)),
                ('assigned', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Months',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredStudents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Examination')),
            ],
        ),
        migrations.CreateModel(
            name='Regulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regulation', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('student_name', models.CharField(max_length=225)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Department')),
                ('regulation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Regulation')),
                ('student_semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Semester')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subject_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=225)),
                ('drawingType', models.BooleanField(default=False)),
                ('regulation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Regulation')),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('set_number', models.IntegerField(default=1)),
                ('max_set', models.IntegerField(default=1)),
                ('examination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Examination')),
                ('regulation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Regulation')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='student_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Year'),
        ),
        migrations.AddField(
            model_name='registeredstudents',
            name='regulation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Regulation'),
        ),
        migrations.AddField(
            model_name='registeredstudents',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Student'),
        ),
        migrations.AddField(
            model_name='registeredstudents',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Subject'),
        ),
        migrations.AddField(
            model_name='registeredstudents',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.ExaminationType'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='capacity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.ClassroomCapacity'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='dept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Department'),
        ),
        migrations.AddField(
            model_name='arrangement',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Classroom'),
        ),
        migrations.AddField(
            model_name='arrangement',
            name='examination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Examination'),
        ),
        migrations.AddField(
            model_name='arrangement',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Student'),
        ),
        migrations.AddField(
            model_name='arrangement',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Examination.Subject'),
        ),
        migrations.AlterUniqueTogether(
            name='timetable',
            unique_together=set([('date', 'subject')]),
        ),
        migrations.AlterUniqueTogether(
            name='registeredstudents',
            unique_together=set([('student', 'subject', 'examination')]),
        ),
        migrations.AlterUniqueTogether(
            name='invigilation',
            unique_together=set([('examination', 'classroom', 'faculty')]),
        ),
        migrations.AlterUniqueTogether(
            name='arrangement',
            unique_together=set([('examination', 'student', 'date', 'subject')]),
        ),
    ]