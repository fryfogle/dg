# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hack4farming', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='date',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='pickupdate',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='date',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
    ]
