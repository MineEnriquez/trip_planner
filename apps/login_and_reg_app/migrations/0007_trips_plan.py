# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-09-20 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_reg_app', '0006_trips_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='trips',
            name='plan',
            field=models.TextField(default='something'),
            preserve_default=False,
        ),
    ]
