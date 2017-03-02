# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loop', '0008_phoneverificationivr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneverificationivr',
            name='call_duration',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
