# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20160317_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='e',
            name='detail_public',
            field=models.CharField(max_length=80, null=True, verbose_name='Title of event, this be shown publicly', blank=True),
        ),
    ]
