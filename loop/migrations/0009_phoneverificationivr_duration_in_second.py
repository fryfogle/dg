# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0008_phoneverificationivr'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneverificationivr',
            name='duration_in_second',
            field=models.FloatField(default=-1),
        ),
    ]
