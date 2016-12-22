# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-20 18:34
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
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=40, null=True)),
                ('last_read', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=100)),
                ('amount', models.FloatField()),
                ('date', models.DateField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='monosaur.Category')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spend_analyser.Session')),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='subscriptions.Subscription')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together=set([('reference', 'amount', 'date', 'session')]),
        ),
    ]
