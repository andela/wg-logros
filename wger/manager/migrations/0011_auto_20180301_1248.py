# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-03-01 09:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_auto_20180301_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutsession',
            name='workout_log',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='manager.WorkoutLog', verbose_name='WorkoutLog'),
        ),
    ]
