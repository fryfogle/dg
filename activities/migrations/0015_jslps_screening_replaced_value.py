# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0014_auto_20170522_0851'),
    ]

    operations = [
        migrations.AddField(
            model_name='jslps_screening',
            name='replaced_value',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
