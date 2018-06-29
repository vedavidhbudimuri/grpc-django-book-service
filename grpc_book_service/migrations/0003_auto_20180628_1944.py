# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-28 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grpc_book_service', '0002_auto_20180628_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_type',
            field=models.CharField(choices=[(b'PAPER_BACK', b'Paper-Back'), (b'HARD_BIND', b'Hard Cover'), (b'ONLINE', b'Online')], max_length=64),
        ),
    ]