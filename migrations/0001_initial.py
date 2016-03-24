# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20160316_2053'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='E',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('e_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date of the event, in the format "yyyy-mm-dd", e.g. for 31st December 2015, enter "2015-12-31"')),
                ('detail_public', models.TextField(blank=True, null=True, verbose_name='Details to be shown publicly')),
                ('detail_private', models.TextField(blank=True, null=True, verbose_name='Details to be shown only to logged in users')),
                ('notes', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_live', models.BooleanField(default=True)),
                ('attendees', models.ManyToManyField(related_name='bookedin', to='users.Person', blank=True)),
                ('author', models.ForeignKey(related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
