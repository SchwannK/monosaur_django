# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-16 22:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import monosaur.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', monosaur.models.EmptyStringToNoneField(blank=True, max_length=50, null=True)),
                ('reference', models.CharField(max_length=100, unique=True)),
                ('category', monosaur.models.EmptyForeignKeyToNoneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monosaur.Category')),
            ],
        ),
    ]
