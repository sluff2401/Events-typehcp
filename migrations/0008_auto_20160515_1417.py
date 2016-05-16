# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20160515_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='e',
            name='detail_private',
            field=models.TextField(null=True, verbose_name='Details of event', blank=True),
        ),
    ]
