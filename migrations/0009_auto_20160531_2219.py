# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_auto_20160530_2232'),
        ('events', '0008_auto_20160515_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='e',
            name='hosts',
            field=models.ManyToManyField(blank=True, to='users.Person', related_name='hh'),
        ),
        migrations.AlterField(
            model_name='e',
            name='detail_public',
            field=models.CharField(max_length=80, blank=True, default='', verbose_name='Title of event, this be shown publicly'),
        ),
    ]
