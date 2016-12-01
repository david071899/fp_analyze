# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-01 05:23
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='wordcloud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=2014)),
                ('month', models.IntegerField(default=1)),
                ('word_data', jsonfield.fields.JSONField()),
            ],
        ),
    ]
