# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-03-01 11:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0012_auto_20180301_1321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workoutsession',
            name='workout_log',
        ),
    ]
