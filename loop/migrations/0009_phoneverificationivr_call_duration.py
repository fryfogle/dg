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
            name='call_duration',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
