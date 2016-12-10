# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2016-12-10 11:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('monosaur', '0001_initial'),
        ('subscriptions', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.FloatField()),
                ('date', models.DateField()),
                ('user', models.CharField(max_length=40, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monosaur.Category')),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subscriptions.Subscription')),
            ],
        ),
    ]
