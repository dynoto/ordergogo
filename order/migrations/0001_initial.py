# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('location', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True)),
                ('price', models.FloatField(null=True)),
                ('owner', models.ForeignKey(related_name='item_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('caption', models.CharField(default=b'', max_length=254)),
                ('img_url', models.URLField()),
                ('img_thumb', models.URLField(null=True)),
                ('item', models.ForeignKey(to='order.Item')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True)),
                ('remarks', models.TextField(blank=True)),
                ('is_assigned', models.BooleanField(default=False)),
                ('is_delivered', models.BooleanField(default=False)),
                ('tracking_id', models.CharField(max_length=64, blank=True)),
                ('assigned_to', models.ForeignKey(related_name='order_assigned_to', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField()),
                ('remarks', models.TextField(blank=True)),
                ('order_price', models.FloatField(null=True, blank=True)),
                ('item', models.ForeignKey(to='order.Item')),
                ('order', models.ForeignKey(to='order.Order')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='order.Item', through='order.OrderItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='location_from',
            field=models.ForeignKey(related_name='order_location_from', to='location.Address'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='location_to',
            field=models.ForeignKey(related_name='order_location_to', to='location.Address'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(related_name='order_owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
