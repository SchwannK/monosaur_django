# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-16 17:41
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
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='monosaur.Category'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='spend_analyser.Session'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='subscriptions.Subscription'),
        ),
    ]