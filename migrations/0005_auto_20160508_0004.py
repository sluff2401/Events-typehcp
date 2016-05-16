# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20160506_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='e',
            name='attendees',
            field=models.ManyToManyField(blank=True, related_name='bookedin', to='users.Person'),
        ),
    ]
