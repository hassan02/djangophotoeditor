# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 23:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0002_auto_20160909_1518'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='size',
            new_name='image_size',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='name',
        ),
        migrations.AddField(
            model_name='photo',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
