# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 22:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spend_analyser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spend_analyser.Session'),
        ),
    ]