# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gps_location', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True)),
                ('address_name', models.CharField(default=b'', max_length=255, blank=True)),
                ('address_line_1', models.CharField(default=b'', max_length=255, blank=True)),
                ('address_line_2', models.CharField(default=b'', max_length=255, blank=True)),
                ('postal_code', models.CharField(default=b'', max_length=255, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(related_name='address_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
            bases=(models.Model,),
        ),
    ]
