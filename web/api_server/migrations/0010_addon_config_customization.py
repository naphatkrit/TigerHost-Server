# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-29 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_server', '0009_addon_display_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='addon',
            name='config_customization',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
