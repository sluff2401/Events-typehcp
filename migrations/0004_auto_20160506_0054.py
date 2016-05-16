# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20160327_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='e',
            name='detail_private',
            field=models.CharField(verbose_name='Details to be shown only to logged in users', null=True, max_length=200, blank=True),
        ),
    ]
