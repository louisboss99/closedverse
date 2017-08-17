# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-16 23:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('closedverse_main', '0015_remove_community_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='tags',
            field=models.CharField(blank=True, choices=[('announcements', 'main announcement community'), ('changelog', 'main changelog')], max_length=255, null=True),
        ),
    ]