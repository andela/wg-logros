# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-03-01 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0002_meal_meal_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='mealitem',
            name='meal_choice',
            field=models.CharField(choices=[('PL', 'Planned'), ('CO', 'Consumed')], default='PL', max_length=2),
        ),
    ]
