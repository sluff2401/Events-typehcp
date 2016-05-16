# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20160508_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='e',
            name='detail_private',
            field=models.TextField(verbose_name='Details of event', blank=True, null=True),
        ),
    ]
