# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-01 21:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam2', '0002_quote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='favorites',
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]