# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20160515_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='e',
            name='detail_private',
            field=models.CharField(verbose_name='Details of event', null=True, max_length=1000, blank=True),
        ),
    ]
