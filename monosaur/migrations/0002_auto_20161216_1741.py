# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-16 17:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import monosaur.models


class Migration(migrations.Migration):

    dependencies = [
        ('monosaur', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixturecompany',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='monosaur.Category'),
        ),
        migrations.AlterField(
            model_name='fixturecompany',
            name='name',
            field=monosaur.models.EmptyStringToNoneField(blank=True, max_length=50, null=True),
        ),
    ]