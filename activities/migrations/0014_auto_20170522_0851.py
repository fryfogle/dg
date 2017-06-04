# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0013_auto_20170522_0606'),
    ]

    operations = [
        migrations.AddField(
            model_name='personadoptpractice',
            name='adopt_practice_second',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'1', b'Yes'), (b'2', b'No'), (b'3', b'Not Applicable')]),
        ),
    ]